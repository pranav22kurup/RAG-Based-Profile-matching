# RAG-Based Resume Matching System

This project implements an end-to-end Retrieval-Augmented Generation (RAG) pipeline for resume-to-job matching.
It covers document chunking, embedding generation, vector database indexing, semantic retrieval, hybrid ranking, strict hard-filtering, and evaluation.

## 1. Project Objectives

- Implement document chunking and embedding
- Build vector databases for similarity search
- Create retrieval and ranking pipelines
- Understand and evaluate semantic search quality

## 2. Assignment Coverage

### Part A: RAG System Setup

Implemented in `resume_rag.py`.

- Resume ingestion from filesystem (`resumes/`)
- Section-aware chunking (Experience, Education, Skills, etc.)
- Embedding generation:
  - HuggingFace (`all-MiniLM-L6-v2`) via Chroma embedding function
  - Optional OpenAI embedding function
  - TF-IDF fallback for offline/local environments
- Vector storage in ChromaDB (persistent local DB)
- Metadata extraction and storage for filtering:
  - Candidate name
  - Skills
  - Experience years
  - Education level
  - Seniority
  - Per-skill tenure map (`skill_years`)

### Part B: Job Matching Engine

Implemented in `job_matcher.py`.

- Job description parsing
- Semantic retrieval over vector index
- Hybrid ranking (semantic + required skill keywords + preferred skill keywords)
- Scoring on 0-100 scale
- Match reasoning and relevant text excerpts
- Hard-filter enforcement for must-have requirements
  - Strict per-skill tenure checks for requirements like `5+ years Python`

### Output Format

The matching output follows the required JSON shape:

```json
{
  "job_description": "...",
  "top_matches": [
    {
      "candidate_name": "John Doe",
      "resume_path": "resumes/john_doe.pdf",
      "match_score": 92,
      "matched_skills": ["Python", "Machine Learning"],
      "relevant_excerpts": ["..."],
      "reasoning": "Strong match for ML experience..."
    }
  ]
}
```

## 3. Repository Structure

- `resume_rag.py` - RAG indexing pipeline and metadata extraction
- `job_matcher.py` - Retrieval, hybrid scoring, hard filters, final ranking
- `generate_resumes.py` - Synthetic resume dataset generator (33 resumes)
- `generate_jds.py` - Job description generator (8 job descriptions)
- `rag_analysis_notebook.ipynb` - Experimentation, evaluation, and visual analysis
- `results_*.json` - Matching outputs for generated job descriptions
- `resumes/` - Resume corpus
- `job_descriptions/` - Job description corpus
- `chroma_db/` - Persistent Chroma vector store (generated)

## 4. Data and Deliverables

### Dataset

- 33 diverse resumes (exceeds 30+ requirement)
- 8 job descriptions (exceeds 5+ requirement)

### Notebook Deliverables

`rag_analysis_notebook.ipynb` includes:

- Chunking analysis
- Dataset analysis
- Retrieval accuracy metrics (Recall@K)
- Latency benchmarks
- Score distribution analysis
- Hybrid component contribution analysis
- Sample output formatting
- Conclusions and production recommendations

## 5. Technical Architecture

### 5.1 Document Processing

1. Load resume text (`.txt`, basic `.pdf` support)
2. Split into semantic sections using section headers
3. Create chunks:
   - Full-document chunk
   - Section chunks
   - Sub-chunks for long sections
4. Extract metadata per resume
5. Add chunks + metadata to ChromaDB collection

### 5.2 Embeddings

Configured in `get_chroma_collection()`.

Priority order:

1. OpenAI embeddings (if API key + flag provided)
2. HuggingFace sentence-transformers (`all-MiniLM-L6-v2`) (default path)
3. TF-IDF local fallback

### 5.3 Retrieval and Ranking

1. Parse JD requirements and skills
2. Embed/query JD against ChromaDB
3. Aggregate chunk-level hits to candidate-level signals
4. Score candidates with weighted hybrid formula:

- Semantic: 50%
- Required skills: 30%
- Preferred skills: 10%
- Seniority alignment: 5%
- Education alignment: 5%

5. Apply strict hard filters for explicit `X+ years <skill>` requirements
6. Return ranked top-K matches

## 6. Hard Filter and Per-Skill Tenure Logic

Recent rubric-alignment improvements:

- Added stricter per-skill tenure estimation in `resume_rag.py`:
  - Job-date block detection from resume timelines
  - Skill alias handling (`node.js/nodejs`, `scikit-learn/sklearn`, etc.)
  - Boundary-aware regex matching for higher precision
- Added stricter `years requirement` parsing in `job_matcher.py`:
  - Better handling of multi-word skills (e.g., `machine learning`)
  - Canonical skill normalization
- Updated hard filters to enforce per-skill tenure directly for explicit must-have year constraints

## 7. Security and Privacy Notes

Current posture (good for local academic project):

- ChromaDB is local and persistent by default
- HuggingFace embedding path runs locally after model download

Recommended hardening for production:

- Encrypt vector store at rest
- Restrict filesystem permissions on `chroma_db/`
- Remove runtime package installation in notebooks for controlled environments
- Add PII redaction before indexing resumes
- Keep all API keys in environment variables only

## 8. Setup Instructions

## 8.1 Prerequisites

- Python 3.11+ (project was validated on 3.11 and 3.12)
- Windows/macOS/Linux

## 8.2 Install Dependencies

```bash
pip install chromadb numpy scikit-learn sentence-transformers PyPDF2 matplotlib
```

Optional (for OpenAI embedding mode):

```bash
pip install openai
```

## 8.3 Generate Dataset (if needed)

```bash
python generate_resumes.py
python generate_jds.py
```

## 9. How to Run

## 9.1 Build/Refresh Vector Index

HuggingFace + ChromaDB:

```bash
python -c "from resume_rag import build_rag_index; build_rag_index(resumes_dir='./resumes', persist_dir='./chroma_db', collection_name='resumes_hf', use_huggingface=True, force_rebuild=True)"
```

## 9.2 Run Matching from CLI

```bash
python job_matcher.py --jd job_descriptions/senior_ml_engineer.txt --resumes-dir ./resumes --persist-dir ./chroma_db --top-k 10 --output-json results_senior_ml_engineer.json
```

## 9.3 Run Notebook Analysis

Open and execute:

- `rag_analysis_notebook.ipynb`

Recommended order:

1. Imports/setup
2. Build/load index
3. Chunking/dataset analysis
4. Retrieval evaluation
5. Score/hybrid analysis
6. Sample output + conclusions

## 10. Verification Checklist

- Imports cell executes successfully
- Index build prints HuggingFace backend
- Index stats show non-zero resume and chunk counts
- Retrieval evaluation prints Recall@K and latency stats
- Sample output cell prints required JSON structure
- `results_*.json` files are generated

## 11. Known Limitations

- Per-skill tenure estimation is heuristic (resume text quality dependent)
- PDF parsing may be noisy for complex layouts
- Current retrieval does not use a neural re-ranker
- Chroma local mode is not a distributed production deployment

## 12. Future Improvements

- Add Cohere embedding backend option
- Cross-encoder reranking for top-N candidates
- Better skill ontology and normalization
- Enterprise-grade security controls (encryption, audit, access control)
- Human-in-the-loop calibration for score interpretability

## 13. Authors and Purpose

This repository is an educational implementation for resume-job semantic matching using RAG principles and vector search.
It is designed to satisfy coursework requirements while remaining extensible toward production architecture.
