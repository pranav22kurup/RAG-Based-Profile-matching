"""
resume_rag.py — RAG System for Resume Processing

Part A: Document Processing Pipeline
- Load resumes from filesystem
- Chunk documents intelligently (preserve sections)
- Generate embeddings using scikit-learn TF-IDF + optional OpenAI
- Store in ChromaDB vector database with metadata
"""

import os
import re
import json
import hashlib
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

import numpy as np # type: ignore
import chromadb # type: ignore
from chromadb.utils import embedding_functions # type: ignore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# 1. SECTION-AWARE CHUNKING
# ─────────────────────────────────────────────

SECTION_HEADERS = [
    r"SUMMARY|OBJECTIVE|PROFILE|ABOUT",
    r"EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT|PROFESSIONAL EXPERIENCE",
    r"EDUCATION|ACADEMIC",
    r"SKILLS|TECHNICAL SKILLS|CORE COMPETENCIES",
    r"PROJECTS|PERSONAL PROJECTS|SIDE PROJECTS",
    r"PUBLICATIONS|RESEARCH|PAPERS",
    r"CERTIFICATIONS|CERTIFICATES|LICENSES",
    r"AWARDS|HONORS|ACHIEVEMENTS",
]
SECTION_PATTERN = re.compile(
    r"^(" + "|".join(SECTION_HEADERS) + r")\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def split_into_sections(text: str) -> dict[str, str]:
    """Split resume text into named sections."""
    sections = {}
    lines = text.strip().splitlines()
    
    # Header = everything before first section keyword (name, contact)
    header_lines = []
    current_section = None
    current_lines = []

    for line in lines:
        stripped = line.strip()
        if SECTION_PATTERN.match(stripped):
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            elif header_lines or current_lines:
                sections["HEADER"] = "\n".join(header_lines + current_lines).strip()
            current_section = stripped.upper()
            current_lines = []
        else:
            if current_section is None:
                header_lines.append(line)
            else:
                current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()
    elif header_lines:
        sections["HEADER"] = "\n".join(header_lines).strip()

    return {k: v for k, v in sections.items() if v}


def chunk_resume(text: str, resume_name: str, chunk_size: int = 800) -> list[dict]:
    """
    Chunk a resume into semantically meaningful pieces.
    Strategy: one chunk per section; long sections are sub-chunked by paragraph.
    Returns list of dicts with keys: chunk_id, text, section, char_start.
    """
    sections = split_into_sections(text)
    chunks = []

    # Always include a full-document chunk for holistic matching
    chunks.append({
        "chunk_id": f"{resume_name}::FULL",
        "text": text[:3000],  # cap to avoid token overload
        "section": "FULL",
        "char_start": 0,
    })

    for section_name, section_text in sections.items():
        if len(section_text) <= chunk_size:
            chunks.append({
                "chunk_id": f"{resume_name}::{section_name}",
                "text": section_text,
                "section": section_name,
                "char_start": text.find(section_text),
            })
        else:
            # Sub-chunk long sections by paragraph
            paragraphs = re.split(r"\n{2,}", section_text)
            current = []
            current_len = 0
            sub_idx = 0
            for para in paragraphs:
                if current_len + len(para) > chunk_size and current:
                    chunk_text = "\n\n".join(current)
                    chunks.append({
                        "chunk_id": f"{resume_name}::{section_name}::{sub_idx}",
                        "text": chunk_text,
                        "section": section_name,
                        "char_start": text.find(chunk_text),
                    })
                    sub_idx += 1
                    current = [para]
                    current_len = len(para)
                else:
                    current.append(para)
                    current_len += len(para)
            if current:
                chunk_text = "\n\n".join(current)
                chunks.append({
                    "chunk_id": f"{resume_name}::{section_name}::{sub_idx}",
                    "text": chunk_text,
                    "section": section_name,
                    "char_start": text.find(chunk_text),
                })

    return chunks


# ─────────────────────────────────────────────
# 2. METADATA EXTRACTION
# ─────────────────────────────────────────────

SKILL_KEYWORDS = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "go", "rust", "scala",
    "kotlin", "swift", "r", "sql", "bash", "matlab", "cuda",
    # ML/AI
    "machine learning", "deep learning", "nlp", "computer vision", "pytorch", "tensorflow",
    "scikit-learn", "xgboost", "hugging face", "langchain", "transformers", "llm",
    "reinforcement learning", "rag", "bert", "gpt", "llama",
    # Data
    "spark", "kafka", "airflow", "dbt", "snowflake", "bigquery", "redshift",
    "elasticsearch", "hadoop", "flink", "databricks",
    # Cloud
    "aws", "gcp", "azure", "kubernetes", "docker", "terraform", "helm",
    # Web
    "react", "node.js", "fastapi", "django", "flask", "graphql", "rest",
    "next.js", "vue.js", "typescript",
    # Databases
    "postgresql", "mysql", "mongodb", "redis", "cassandra", "dynamodb",
    # Other
    "solidity", "ros", "rlhf", "mlops", "devops", "sre",
]

DEGREE_PATTERN = re.compile(
    r"(B\.?S\.?|M\.?S\.?|Ph\.?D\.?|B\.?A\.?|M\.?B\.?A\.?|M\.?Eng\.?)\b",
    re.IGNORECASE,
)
YEAR_RANGE_PATTERN = re.compile(r"(\d{4})\s*[–\-]\s*(\d{4}|Present)", re.IGNORECASE)
# Match ALL CAPS names first ("ALICE CHEN"), then title-case ("Alice Chen")
ALL_CAPS_NAME_PATTERN = re.compile(r"^([A-Z][A-Z]+(?:\s[A-Z][A-Z']+){1,3})\s*$", re.MULTILINE)
TITLE_CASE_NAME_PATTERN = re.compile(r"^([A-Z][a-z]+(?:\s[A-Z][a-z']+){1,3})", re.MULTILINE)
# Pattern to identify job entries with date ranges for per-skill year extraction
JOB_ENTRY_PATTERN = re.compile(
    r"^(.+?)\s*\|\s*(.+?)\s*\|\s*(\d{4})\s*[–\-]\s*(\d{4}|Present)",
    re.MULTILINE | re.IGNORECASE,
)

# Canonical skill -> aliases that appear in resumes/JDs.
SKILL_ALIASES = {
    "node.js": ["nodejs"],
    "next.js": ["nextjs"],
    "vue.js": ["vuejs"],
    "scikit-learn": ["sklearn"],
    "hugging face": ["huggingface"],
    "c++": ["cpp"],
}


def _skill_patterns(skill: str) -> list[re.Pattern]:
    """Compile strict match patterns for a canonical skill and aliases."""
    variants = [skill.lower(), *SKILL_ALIASES.get(skill.lower(), [])]
    patterns = []
    for item in variants:
        escaped = re.escape(item)
        patterns.append(re.compile(rf"(?<!\w){escaped}(?!\w)", re.IGNORECASE))
    return patterns


def _contains_skill(text: str, skill: str) -> bool:
    """Return True if a skill (or alias) is present as a bounded token/phrase."""
    for pattern in _skill_patterns(skill):
        if pattern.search(text):
            return True
    return False


def _estimate_skill_years(text: str, skills: list[str]) -> dict[str, int]:
    """
    Estimate per-skill years by matching skills within dated job blocks
    and summing durations where each skill is explicitly mentioned.
    """
    current_year = datetime.now().year
    # Split resume into job entry blocks using the date-range pattern
    entries = JOB_ENTRY_PATTERN.finditer(text)
    job_blocks: list[tuple[int, str]] = []  # (duration, block_text)

    positions = [(m.start(), m.group(3), m.group(4)) for m in entries]

    for idx, (pos, start_str, end_str) in enumerate(positions):
        start_yr = int(start_str)
        end_yr = current_year if "present" in end_str.lower() else int(end_str)
        duration = max(end_yr - start_yr, 1)

        # Grab text from this entry until the next entry (or 1500 chars)
        if idx + 1 < len(positions):
            block = text[pos : positions[idx + 1][0]]
        else:
            block = text[pos : pos + 1500]

        job_blocks.append((duration, block.lower()))

    skill_years: dict[str, int] = {}
    for skill in skills:
        total = sum(dur for dur, block in job_blocks if _contains_skill(block, skill))
        if total > 0:
            skill_years[skill] = total

    return skill_years


def extract_metadata(text: str, filename: str) -> dict:
    """Extract structured metadata from resume text."""
    meta = {}

    # Name — try ALL CAPS first (most resumes), then title-case, then fallback
    name_match = ALL_CAPS_NAME_PATTERN.search(text[:300])
    if name_match:
        meta["name"] = name_match.group(1).title()  # normalise to title-case
    else:
        name_match = TITLE_CASE_NAME_PATTERN.search(text[:300])
        if name_match:
            meta["name"] = name_match.group(1)
        else:
            meta["name"] = Path(filename).stem.replace("_", " ").title()

    # Education level
    degrees = DEGREE_PATTERN.findall(text)
    if any("ph" in d.lower() for d in degrees):
        meta["education_level"] = "PhD"
    elif any(d.lower() in ("m.s.", "ms", "m.s", "mba", "m.b.a.") for d in degrees):
        meta["education_level"] = "Masters"
    elif degrees:
        meta["education_level"] = "Bachelors"
    else:
        meta["education_level"] = "Unknown"

    # Years of experience (from date ranges)
    year_ranges = YEAR_RANGE_PATTERN.findall(text)
    if year_ranges:
        current_year = datetime.now().year
        start_years = [int(y[0]) for y in year_ranges]
        end_years = [current_year if "present" in y[1].lower() else int(y[1]) for y in year_ranges]
        earliest_start = min(start_years)
        latest_end = max(end_years)
        meta["experience_years"] = latest_end - earliest_start
    else:
        meta["experience_years"] = 0

    # Skills
    text_lower = text.lower()
    found_skills = [skill for skill in SKILL_KEYWORDS if skill in text_lower]
    meta["skills"] = found_skills
    meta["skills_str"] = ", ".join(found_skills)  # ChromaDB needs string metadata

    # Per-skill experience years (approximate from job entries)
    meta["skill_years"] = _estimate_skill_years(text, found_skills)

    # Seniority heuristic
    if meta["experience_years"] >= 10 or "staff" in text_lower or "principal" in text_lower:
        meta["seniority"] = "Staff/Principal"
    elif meta["experience_years"] >= 6 or "senior" in text_lower:
        meta["seniority"] = "Senior"
    elif meta["experience_years"] >= 3:
        meta["seniority"] = "Mid"
    else:
        meta["seniority"] = "Junior"

    meta["filename"] = filename
    meta["char_count"] = len(text)

    return meta


# ─────────────────────────────────────────────
# 3. CHROMA DB SETUP
# ─────────────────────────────────────────────

def get_chroma_collection(
    persist_dir: str = "./chroma_db",
    collection_name: str = "resumes",
    use_openai: bool = False,
    openai_api_key: Optional[str] = None,
    use_huggingface: bool = True,  # Added parameter
) -> chromadb.Collection:
    """
    Create or load a ChromaDB collection.
    Uses OpenAI embeddings if key provided, else defaults to HuggingFace
    (all-MiniLM-L6-v2), else falls back to local TF-IDF.
    """
    client = chromadb.PersistentClient(path=persist_dir)

    if use_openai and openai_api_key:
        ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=openai_api_key,
            model_name="text-embedding-3-small",
        )
        logger.info("Using OpenAI text-embedding-3-small")
    elif use_huggingface:
        # Load the HuggingFace sentence-transformers default (all-MiniLM-L6-v2)
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction # type: ignore
        ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        logger.info("Using HuggingFace all-MiniLM-L6-v2 embeddings")
    else:
        # TF-IDF embedding (no external download required)
        ef = TFIDFEmbeddingFunction(persist_dir=persist_dir)
        logger.info("Using TF-IDF embedding function (512-dim, no download required)")

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


# ─────────────────────────────────────────────
# 4. TF-IDF FALLBACK EMBEDDING FUNCTION
# ─────────────────────────────────────────────

class TFIDFEmbeddingFunction(chromadb.EmbeddingFunction):
    """
    Lightweight TF-IDF based embedding for environments without sentence-transformers.
    Produces 512-dim sparse-dense vectors.
    Uses a shared global vocabulary so all calls (index + query) produce same-dim vectors.
    """
    # Shared global vocabulary built from a broad corpus of tech/resume terms
    _GLOBAL_VOCAB = [
        # Programming languages
        "python", "java", "javascript", "typescript", "scala", "kotlin", "swift",
        "golang", "rust", "cpp", "cuda", "matlab", "bash", "sql", "perl",
        # ML/AI
        "machine", "learning", "deep", "neural", "network", "model", "training",
        "inference", "embedding", "transformer", "pytorch", "tensorflow", "keras",
        "scikit", "xgboost", "lightgbm", "hugging", "face", "bert", "gpt", "llm",
        "llama", "nlp", "natural", "language", "processing", "computer", "vision",
        "reinforcement", "classification", "regression", "clustering", "recommendation",
        "retrieval", "augmented", "generation", "rag", "vector", "database", "chroma",
        "pinecone", "weaviate", "langchain", "llamaindex", "openai", "anthropic",
        "fine", "tuning", "rlhf", "lora", "quantization", "distillation", "onnx",
        # Data Engineering
        "spark", "kafka", "flink", "hadoop", "hive", "airflow", "prefect", "dbt",
        "snowflake", "bigquery", "redshift", "databricks", "delta", "iceberg",
        "etl", "elt", "pipeline", "warehouse", "lakehouse", "streaming",
        # Cloud/DevOps
        "aws", "gcp", "azure", "kubernetes", "docker", "terraform", "helm", "istio",
        "argocd", "jenkins", "github", "actions", "cicd", "sre", "devops", "platform",
        "prometheus", "grafana", "datadog", "monitoring", "observability",
        # Databases
        "postgresql", "mysql", "mongodb", "redis", "cassandra", "dynamodb", "elasticsearch",
        # Web
        "react", "nodejs", "fastapi", "django", "flask", "graphql", "rest", "grpc",
        "nextjs", "vuejs", "typescript", "html", "css", "frontend", "backend",
        # Roles/Experience
        "senior", "junior", "staff", "principal", "lead", "manager", "director",
        "engineer", "scientist", "analyst", "architect", "developer", "researcher",
        "years", "experience", "team", "leadership", "mentoring", "design", "system",
        # Skills/Concepts
        "distributed", "systems", "microservices", "serverless", "event", "driven",
        "scalable", "high", "availability", "performance", "optimization", "security",
        "agile", "scrum", "product", "roadmap", "strategy", "analytics", "metrics",
        "production", "deployment", "migration", "integration", "api", "sdk",
        # Education
        "phd", "masters", "bachelor", "stanford", "mit", "berkeley", "carnegie",
        "computer", "science", "mathematics", "statistics", "engineering", "physics",
        # Specializations
        "robotics", "ros", "lidar", "autonomous", "blockchain", "solidity", "defi",
        "cybersecurity", "penetration", "testing", "compliance", "hipaa", "gdpr",
        "quantitative", "finance", "trading", "bioinformatics", "genomics", "mobile",
        "ios", "android", "swift", "swiftui", "jetpack", "compose",
    ]

    def __init__(self, n_features: int = 512, persist_dir: Optional[str] = None):
        import pickle
        from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
        self.n_features = n_features
        self.persist_dir = persist_dir
        self._pickle_path = os.path.join(persist_dir, "tfidf_vectorizer.pkl") if persist_dir else None

        # Try to load persisted vectorizer
        if self._pickle_path and os.path.exists(self._pickle_path):
            with open(self._pickle_path, "rb") as f:
                self.vectorizer = pickle.load(f)
            self._fitted = True
        else:
            self.vectorizer = TfidfVectorizer(
                max_features=n_features,
                ngram_range=(1, 2),
                sublinear_tf=True,
                min_df=1,
                vocabulary=None,  # will be set after fitting
            )
            # Pre-fit on global vocabulary seed
            seed_docs = [
                " ".join(self._GLOBAL_VOCAB),
                " ".join(self._GLOBAL_VOCAB[:len(self._GLOBAL_VOCAB)//2]),
                " ".join(self._GLOBAL_VOCAB[len(self._GLOBAL_VOCAB)//2:]),
            ]
            self.vectorizer.fit(seed_docs)
            self._fitted = True
            self._save()

    def _save(self):
        import pickle
        if self._pickle_path:
            os.makedirs(os.path.dirname(self._pickle_path), exist_ok=True)
            with open(self._pickle_path, "wb") as f:
                pickle.dump(self.vectorizer, f)

    def refit(self, texts: list[str]):
        """Refit vectorizer on the full corpus and save."""
        from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
        seed_docs = [" ".join(self._GLOBAL_VOCAB)] + texts
        new_vect = TfidfVectorizer(
            max_features=self.n_features,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1,
        )
        new_vect.fit(seed_docs)
        self.vectorizer = new_vect
        self._fitted = True
        self._save()

    def __call__(self, texts: list[str]) -> list[list[float]]:
        matrix = self.vectorizer.transform(texts)
        dense = matrix.toarray()
        # L2-normalize
        norms = np.linalg.norm(dense, axis=1, keepdims=True)
        norms[norms == 0] = 1
        dense = dense / norms
        return dense.tolist()


# ─────────────────────────────────────────────
# 5. MAIN PIPELINE
# ─────────────────────────────────────────────

def load_resume(filepath: str) -> str:
    """Load a resume file (supports .txt; extend for .pdf, .docx)."""
    filepath = Path(filepath) # type: ignore
    if filepath.suffix.lower() == ".txt": # type: ignore
        return filepath.read_text(encoding="utf-8") # type: ignore
    elif filepath.suffix.lower() == ".pdf": # type: ignore
        try:
            import PyPDF2 # type: ignore
            text = ""
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            logger.warning("PyPDF2 not available; skipping PDF: %s", filepath)
            return ""
    else:
        # Try reading as text
        try:
            return filepath.read_text(encoding="utf-8", errors="ignore") # type: ignore
        except Exception as e:
            logger.error("Cannot read %s: %s", filepath, e)
            return ""


def build_rag_index(
    resumes_dir: str = "./resumes",
    persist_dir: str = "./chroma_db",
    collection_name: str = "resumes",
    use_openai: bool = False,
    openai_api_key: Optional[str] = None,
    use_huggingface: bool = True,  # Added parameter
    force_rebuild: bool = False,
) -> tuple[chromadb.Collection, dict]:
    """
    Full pipeline: load resumes → chunk → embed → store in ChromaDB.
    Returns (collection, metadata_store).
    """
    logger.info("=== Building RAG Index ===")
    collection = get_chroma_collection(persist_dir, collection_name, use_openai, openai_api_key, use_huggingface)
    
    # Check if already indexed
    existing_count = collection.count()
    if existing_count > 0 and not force_rebuild:
        logger.info("Collection already has %d chunks. Skipping re-index (use force_rebuild=True to redo).", existing_count)
        metadata_store = _load_metadata_store(persist_dir)
        return collection, metadata_store

    # Clear existing if rebuilding
    if force_rebuild and existing_count > 0:
        logger.info("Force rebuild: clearing existing collection...")
        client = chromadb.PersistentClient(path=persist_dir)
        client.delete_collection(collection_name)
        collection = get_chroma_collection(persist_dir, collection_name, use_openai, openai_api_key, use_huggingface)

    metadata_store = {}
    resume_dir = Path(resumes_dir)
    resume_files = list(resume_dir.glob("*.txt")) + list(resume_dir.glob("*.pdf")) + list(resume_dir.glob("*.docx"))

    if not resume_files:
        raise FileNotFoundError(f"No resume files found in {resumes_dir}")

    logger.info("Found %d resume files.", len(resume_files))

    all_ids = []
    all_docs = []
    all_metas = []

    for resume_path in resume_files:
        filename = resume_path.name
        logger.info("  Processing: %s", filename)

        text = load_resume(str(resume_path))
        if not text.strip():
            logger.warning("  Empty file, skipping: %s", filename)
            continue

        # Extract metadata
        meta = extract_metadata(text, filename)
        meta["resume_path"] = str(resume_path)
        metadata_store[filename] = meta

        # Chunk document
        chunks = chunk_resume(text, filename)
        logger.info("    → %d chunks, skills: %s", len(chunks), meta.get("skills_str", "")[:60])

        for chunk in chunks:
            chunk_id = hashlib.md5(chunk["chunk_id"].encode()).hexdigest()[:16]
            chunk_meta = {
                "filename": filename,
                "resume_path": str(resume_path),
                "section": chunk["section"],
                "candidate_name": meta.get("name", "Unknown"),
                "education_level": meta.get("education_level", "Unknown"),
                "experience_years": meta.get("experience_years", 0),
                "seniority": meta.get("seniority", "Unknown"),
                "skills_str": meta.get("skills_str", ""),
                "char_count": len(chunk["text"]),
            }
            all_ids.append(chunk_id)
            all_docs.append(chunk["text"])
            all_metas.append(chunk_meta)

    # Refit TF-IDF on full corpus so query-time vocab matches
    if hasattr(collection._embedding_function, "refit") and all_docs:
        logger.info("Refitting TF-IDF vectorizer on full corpus (%d docs)...", len(all_docs))
        collection._embedding_function.refit(all_docs)

    # Deduplicate IDs (in case of hash collisions)
    seen = set()
    uniq_ids, uniq_docs, uniq_metas = [], [], []
    for i, doc_id in enumerate(all_ids):
        if doc_id not in seen:
            seen.add(doc_id)
            uniq_ids.append(doc_id)
            uniq_docs.append(all_docs[i])
            uniq_metas.append(all_metas[i])

    # Batch upsert into ChromaDB
    BATCH_SIZE = 50
    for i in range(0, len(uniq_ids), BATCH_SIZE):
        collection.add(
            ids=uniq_ids[i:i+BATCH_SIZE],
            documents=uniq_docs[i:i+BATCH_SIZE],
            metadatas=uniq_metas[i:i+BATCH_SIZE],
        )
        logger.info("  Indexed batch %d-%d / %d", i, min(i+BATCH_SIZE, len(uniq_ids)), len(uniq_ids))

    logger.info("✅ Indexed %d total chunks from %d resumes.", len(uniq_ids), len(resume_files))

    _save_metadata_store(metadata_store, persist_dir)
    return collection, metadata_store


def _save_metadata_store(store: dict, persist_dir: str):
    os.makedirs(persist_dir, exist_ok=True)
    path = os.path.join(persist_dir, "metadata_store.json")
    # Convert lists to strings for JSON serialization
    json_store = {}
    for k, v in store.items():
        json_store[k] = {key: (", ".join(val) if isinstance(val, list) else val) for key, val in v.items()}
    with open(path, "w") as f:
        json.dump(json_store, f, indent=2)


def _load_metadata_store(persist_dir: str) -> dict:
    path = os.path.join(persist_dir, "metadata_store.json")
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


# ─────────────────────────────────────────────
# 6. STATS & DIAGNOSTICS
# ─────────────────────────────────────────────

def index_stats(collection: chromadb.Collection, metadata_store: dict) -> dict:
    total_chunks = collection.count()
    total_resumes = len(metadata_store)
    seniority_counts: dict[str, int] = {}
    edu_counts: dict[str, int] = {}
    for meta in metadata_store.values():
        s = meta.get("seniority", "Unknown")
        seniority_counts[s] = seniority_counts.get(s, 0) + 1
        e = meta.get("education_level", "Unknown")
        edu_counts[e] = edu_counts.get(e, 0) + 1

    stats = {
        "total_resumes": total_resumes,
        "total_chunks": total_chunks,
        "avg_chunks_per_resume": round(total_chunks / max(total_resumes, 1), 1),
        "seniority_distribution": seniority_counts,
        "education_distribution": edu_counts,
    }
    return stats


# ─────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Build resume RAG index")
    parser.add_argument("--resumes-dir", default="./resumes", help="Directory with resume files")
    parser.add_argument("--persist-dir", default="./chroma_db", help="ChromaDB persist directory")
    parser.add_argument("--force-rebuild", action="store_true", help="Force re-indexing")
    parser.add_argument("--openai-key", default=None, help="OpenAI API key for embeddings")
    args = parser.parse_args()

    collection, meta_store = build_rag_index(
        resumes_dir=args.resumes_dir,
        persist_dir=args.persist_dir,
        use_openai=bool(args.openai_key),
        openai_api_key=args.openai_key,
        force_rebuild=args.force_rebuild,
    )

    stats = index_stats(collection, meta_store)
    print("\n📊 Index Statistics:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
