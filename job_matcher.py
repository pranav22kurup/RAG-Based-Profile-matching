"""
job_matcher.py — Job Matching Engine

Part B: Semantic Search + Ranking
- Accept job description as input
- Convert JD to embedding and retrieve top-K resumes from ChromaDB
- Hybrid search: semantic + keyword for critical skills
- Score and rank matches (0–100 scale)
- Provide detailed match reasoning
"""

import re
import json
import time
import logging
from typing import Optional
from pathlib import Path
from collections import defaultdict

import numpy as np
import chromadb

from resume_rag import (
    build_rag_index,
    extract_metadata,
    index_stats,
    load_resume,
    SKILL_KEYWORDS,
    TFIDFEmbeddingFunction,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# 1. JOB DESCRIPTION PARSING
# ─────────────────────────────────────────────

REQUIRED_YEARS_PATTERN = re.compile(
    r"(\d+)\+?\s*years?\s+(?:of\s+)?(?:experience\s+(?:in|with)\s+)?([a-zA-Z\+\.#]+)",
    re.IGNORECASE,
)

MUST_HAVE_PATTERN = re.compile(
    r"(?:required|must[- ]have|mandatory|minimum)[:\s]+(.+?)(?=\n|$)",
    re.IGNORECASE,
)


def parse_job_description(jd_text: str) -> dict:
    """
    Extract structured requirements from job description text.
    Returns: {required_skills, preferred_skills, min_years_map, education_req, ...}
    """
    jd_lower = jd_text.lower()

    # Extract mentioned skills
    mentioned_skills = [s for s in SKILL_KEYWORDS if s in jd_lower]

    # Separate required vs preferred sections
    required_section = ""
    preferred_section = ""
    sections = re.split(r"(preferred|nice to have|bonus|optional)", jd_lower, flags=re.IGNORECASE)
    if len(sections) > 1:
        required_section = sections[0]
        preferred_section = " ".join(sections[1:])
    else:
        required_section = jd_lower

    required_skills = [s for s in SKILL_KEYWORDS if s in required_section]
    preferred_skills = [s for s in SKILL_KEYWORDS if s in preferred_section and s not in required_skills]

    # Extract "X+ years of Y" requirements
    years_requirements = {}
    for match in REQUIRED_YEARS_PATTERN.finditer(jd_text):
        years = int(match.group(1))
        skill = match.group(2).lower().strip(".,;:")
        years_requirements[skill] = years

    # Education requirement
    if "ph.d" in jd_lower or "phd" in jd_lower:
        education_req = "PhD"
    elif "m.s" in jd_lower or " ms " in jd_lower or "master" in jd_lower:
        education_req = "Masters"
    elif "b.s" in jd_lower or "bachelor" in jd_lower:
        education_req = "Bachelors"
    else:
        education_req = None

    # Seniority hint
    if "staff" in jd_lower or "principal" in jd_lower:
        seniority_hint = "Staff/Principal"
    elif "senior" in jd_lower or "lead" in jd_lower:
        seniority_hint = "Senior"
    elif "junior" in jd_lower or "entry" in jd_lower:
        seniority_hint = "Junior"
    else:
        seniority_hint = None

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "all_skills": mentioned_skills,
        "years_requirements": years_requirements,
        "education_req": education_req,
        "seniority_hint": seniority_hint,
    }


# ─────────────────────────────────────────────
# 2. SEMANTIC SEARCH
# ─────────────────────────────────────────────

def semantic_search(
    collection: chromadb.Collection,
    query_text: str,
    top_k: int = 30,
    where_filter: Optional[dict] = None,
) -> list[dict]:
    """Query ChromaDB with semantic similarity."""
    query_params = {
        "query_texts": [query_text],
        "n_results": min(top_k, collection.count()),
        "include": ["documents", "metadatas", "distances"],
    }
    if where_filter:
        query_params["where"] = where_filter

    results = collection.query(**query_params)

    hits = []
    for i in range(len(results["ids"][0])):
        hits.append({
            "id": results["ids"][0][i],
            "document": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
            "semantic_score": max(0.0, 1.0 - results["distances"][0][i]),
        })

    return hits


# ─────────────────────────────────────────────
# 3. KEYWORD SEARCH (hybrid component)
# ─────────────────────────────────────────────

def keyword_score(resume_text: str, required_skills: list[str], preferred_skills: list[str]) -> float:
    """
    Compute keyword match score (0–1) based on skill overlap.
    Required skills count double.
    """
    if not required_skills and not preferred_skills:
        return 0.5
    text_lower = resume_text.lower()
    required_hits = sum(1 for s in required_skills if s in text_lower)
    preferred_hits = sum(1 for s in preferred_skills if s in text_lower)
    max_score = len(required_skills) * 2 + len(preferred_skills)
    actual = required_hits * 2 + preferred_hits
    return actual / max_score if max_score > 0 else 0.5


def extract_matched_skills(resume_text: str, jd_skills: list[str]) -> list[str]:
    """Return list of JD skills found in the resume."""
    text_lower = resume_text.lower()
    return [s.title() for s in jd_skills if s in text_lower]


# ─────────────────────────────────────────────
# 4. MUST-HAVE FILTER
# ─────────────────────────────────────────────

def passes_hard_filters(candidate_meta: dict, jd_parsed: dict) -> tuple[bool, list[str]]:
    """
    Check if a candidate meets hard/must-have requirements.
    Uses per-skill years when available, falls back to total experience.
    Returns (passes: bool, reasons: list[str]).
    """
    failures = []
    skill_years = candidate_meta.get("skill_years", {})
    total_years = candidate_meta.get("experience_years", 0)

    for skill, min_years in jd_parsed["years_requirements"].items():
        # Check per-skill years first; fall back to total experience
        candidate_skill_yrs = skill_years.get(skill, None)
        if candidate_skill_yrs is not None:
            if candidate_skill_yrs < min_years:
                failures.append(
                    f"Requires {min_years}+ yrs {skill} (candidate has ~{candidate_skill_yrs} yrs)"
                )
        elif total_years < min_years:
            failures.append(
                f"Requires {min_years}+ yrs experience (candidate has ~{total_years} yrs)"
            )

    return len(failures) == 0, failures


# ─────────────────────────────────────────────
# 5. CANDIDATE RANKING & SCORING
# ─────────────────────────────────────────────

WEIGHTS = {
    "semantic": 0.50,
    "keyword_required": 0.30,
    "keyword_preferred": 0.10,
    "seniority": 0.05,
    "education": 0.05,
}


def score_candidate(
    semantic_score: float,
    resume_text: str,
    candidate_meta: dict,
    jd_parsed: dict,
) -> tuple[float, dict]:
    """
    Compute a composite 0–100 match score.
    Returns (score: float, breakdown: dict).
    """
    # Semantic component
    s_score = semantic_score * WEIGHTS["semantic"]

    # Keyword components
    req_kw = keyword_score(resume_text, jd_parsed["required_skills"], [])
    pref_kw = keyword_score(resume_text, jd_parsed["preferred_skills"], [])
    kw_req_score = req_kw * WEIGHTS["keyword_required"]
    kw_pref_score = pref_kw * WEIGHTS["keyword_preferred"]

    # Seniority alignment
    seniority_map = {"Junior": 0, "Mid": 1, "Senior": 2, "Staff/Principal": 3}
    jd_seniority = jd_parsed.get("seniority_hint")
    candidate_seniority = candidate_meta.get("seniority", "Mid")
    if jd_seniority:
        jd_s = seniority_map.get(jd_seniority, 1)
        cand_s = seniority_map.get(candidate_seniority, 1)
        seniority_match = max(0.0, 1.0 - abs(jd_s - cand_s) * 0.4)
    else:
        seniority_match = 0.7
    s_seniority = seniority_match * WEIGHTS["seniority"]

    # Education match
    edu_req = jd_parsed.get("education_req")
    edu_map = {"Bachelors": 1, "Masters": 2, "PhD": 3, "Unknown": 1}
    if edu_req:
        jd_edu = edu_map.get(edu_req, 1)
        cand_edu = edu_map.get(candidate_meta.get("education_level", "Bachelors"), 1)
        edu_match = min(1.0, cand_edu / jd_edu)
    else:
        edu_match = 0.8
    s_edu = edu_match * WEIGHTS["education"]

    total = (s_score + kw_req_score + kw_pref_score + s_seniority + s_edu) * 100

    breakdown = {
        "semantic": round(s_score * 100, 1),
        "keyword_required": round(kw_req_score * 100, 1),
        "keyword_preferred": round(kw_pref_score * 100, 1),
        "seniority": round(s_seniority * 100, 1),
        "education": round(s_edu * 100, 1),
        "raw_semantic": round(semantic_score, 3),
        "raw_keyword_req": round(req_kw, 3),
    }

    return round(total, 1), breakdown


def build_reasoning(
    candidate_meta: dict,
    matched_skills: list[str],
    score_breakdown: dict,
    jd_parsed: dict,
    relevant_excerpts: list[str],
) -> str:
    """Generate human-readable match reasoning."""
    name = candidate_meta.get("candidate_name", "Candidate")
    exp = candidate_meta.get("experience_years", 0)
    seniority = candidate_meta.get("seniority", "")
    edu = candidate_meta.get("education_level", "")

    lines = []
    lines.append(f"{name} ({seniority}, ~{exp} yrs exp, {edu})")

    if matched_skills:
        lines.append(f"Matched skills: {', '.join(matched_skills[:10])}")

    semantic_pct = score_breakdown.get("raw_semantic", 0)
    if semantic_pct > 0.7:
        lines.append("Strong semantic alignment with job description.")
    elif semantic_pct > 0.5:
        lines.append("Good semantic alignment with job description.")
    else:
        lines.append("Moderate semantic alignment with job description.")

    req_kw = score_breakdown.get("raw_keyword_req", 0)
    if req_kw > 0.7:
        lines.append("Covers most required skills.")
    elif req_kw > 0.4:
        lines.append("Covers some required skills.")
    else:
        lines.append("Limited coverage of required skills.")

    return " | ".join(lines)


def extract_relevant_excerpts(
    semantic_hits: list[dict],
    candidate_filename: str,
    max_excerpts: int = 3,
) -> list[str]:
    """
    Extract the top-scoring text chunks for a given candidate.
    """
    candidate_hits = [
        h for h in semantic_hits
        if h["metadata"].get("filename") == candidate_filename
    ]
    candidate_hits.sort(key=lambda x: x["semantic_score"], reverse=True)
    excerpts = []
    for hit in candidate_hits[:max_excerpts]:
        text = hit["document"][:300].strip()
        if text:
            excerpts.append(text + ("..." if len(hit["document"]) > 300 else ""))
    return excerpts


# ─────────────────────────────────────────────
# 6. MAIN MATCHING FUNCTION
# ─────────────────────────────────────────────

def match_jobs(
    jd_text: str,
    collection: chromadb.Collection,
    metadata_store: dict,
    top_k: int = 10,
    apply_hard_filters: bool = True,
) -> dict:
    """
    Full matching pipeline for a single job description.
    Returns structured output matching the assignment spec.
    """
    t0 = time.time()

    jd_parsed = parse_job_description(jd_text)
    logger.info("JD Parsed — Required skills: %s", jd_parsed["required_skills"][:8])

    # Semantic search: retrieve many candidates, then rank
    semantic_hits = semantic_search(collection, jd_text, top_k=min(100, collection.count()))
    logger.info("Retrieved %d semantic hits", len(semantic_hits))

    # Aggregate scores per candidate (take max chunk score)
    candidate_best: dict[str, dict] = {}
    for hit in semantic_hits:
        filename = hit["metadata"].get("filename", "")
        if not filename:
            continue
        if filename not in candidate_best or hit["semantic_score"] > candidate_best[filename]["semantic_score"]:
            candidate_best[filename] = hit

    logger.info("Unique candidates after aggregation: %d", len(candidate_best))

    # Load full resume text for each candidate (for keyword scoring)
    resume_texts: dict[str, str] = {}
    for filename in candidate_best:
        resume_path = candidate_best[filename]["metadata"].get("resume_path", "")
        if resume_path and Path(resume_path).exists():
            resume_texts[filename] = load_resume(resume_path)
        else:
            # Use concatenated chunks as fallback
            chunks_for_candidate = [
                h["document"] for h in semantic_hits
                if h["metadata"].get("filename") == filename
            ]
            resume_texts[filename] = " ".join(chunks_for_candidate)

    # Score and rank
    ranked_candidates = []
    for filename, best_hit in candidate_best.items():
        meta = metadata_store.get(filename, best_hit["metadata"])
        # Prefer metadata_store values (richer); fall back to chunk metadata
        chunk_meta = best_hit["metadata"]
        if "candidate_name" not in meta:
            meta["candidate_name"] = meta.get("name", chunk_meta.get("candidate_name", "Unknown"))
        meta.setdefault("seniority", chunk_meta.get("seniority", "Mid"))
        meta.setdefault("education_level", chunk_meta.get("education_level", "Unknown"))
        meta.setdefault("experience_years", chunk_meta.get("experience_years", 0))

        resume_text = resume_texts.get(filename, "")

        # Hard filter check
        passes, filter_failures = passes_hard_filters(meta, jd_parsed)
        if apply_hard_filters and not passes:
            logger.debug("Filtered out %s: %s", filename, filter_failures)
            continue

        # Composite score
        score, breakdown = score_candidate(
            best_hit["semantic_score"],
            resume_text,
            meta,
            jd_parsed,
        )

        matched_skills = extract_matched_skills(resume_text, jd_parsed["all_skills"])
        relevant_excerpts = extract_relevant_excerpts(semantic_hits, filename, max_excerpts=3)
        reasoning = build_reasoning(meta, matched_skills, breakdown, jd_parsed, relevant_excerpts)

        ranked_candidates.append({
            "candidate_name": meta["candidate_name"],
            "resume_path": meta.get("resume_path", filename),
            "match_score": score,
            "matched_skills": matched_skills[:15],
            "relevant_excerpts": relevant_excerpts,
            "reasoning": reasoning,
            "score_breakdown": breakdown,
            "seniority": meta["seniority"],
            "experience_years": meta["experience_years"],
            "education_level": meta["education_level"],
            "filter_failures": filter_failures,
        })

    # Sort by score desc
    ranked_candidates.sort(key=lambda x: x["match_score"], reverse=True)
    top_matches = ranked_candidates[:top_k]

    latency_ms = round((time.time() - t0) * 1000, 1)

    result = {
        "job_description": jd_text[:300] + ("..." if len(jd_text) > 300 else ""),
        "jd_required_skills": jd_parsed["required_skills"],
        "jd_preferred_skills": jd_parsed["preferred_skills"],
        "total_candidates_evaluated": len(candidate_best),
        "top_matches": top_matches,
        "latency_ms": latency_ms,
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }
    return result


def match_from_file(
    jd_path: str,
    collection: chromadb.Collection,
    metadata_store: dict,
    top_k: int = 10,
) -> dict:
    """Convenience wrapper: match from a JD file path."""
    jd_text = Path(jd_path).read_text()
    return match_jobs(jd_text, collection, metadata_store, top_k=top_k)


def print_results(result: dict, verbose: bool = True):
    """Pretty-print matching results."""
    print("\n" + "="*70)
    print(f"JOB DESCRIPTION (excerpt): {result['job_description'][:150]}...")
    print(f"Required skills detected: {', '.join(result['jd_required_skills'][:8])}")
    print(f"Candidates evaluated: {result['total_candidates_evaluated']}")
    print(f"Retrieval latency: {result['latency_ms']}ms")
    print(f"\nTOP {len(result['top_matches'])} MATCHES:")
    print("="*70)

    for rank, match in enumerate(result["top_matches"], 1):
        print(f"\n#{rank}. {match['candidate_name']} — Score: {match['match_score']}/100")
        print(f"   Path:       {match['resume_path']}")
        print(f"   Seniority:  {match['seniority']} | Exp: {match['experience_years']} yrs | Edu: {match['education_level']}")
        print(f"   Skills:     {', '.join(match['matched_skills'][:8])}")
        print(f"   Reasoning:  {match['reasoning'][:120]}")
        if verbose and match["relevant_excerpts"]:
            print(f"   Excerpt:    {match['relevant_excerpts'][0][:120]}...")
        if verbose:
            bd = match["score_breakdown"]
            print(f"   Breakdown:  semantic={bd['semantic']} | kw_req={bd['keyword_required']} | kw_pref={bd['keyword_preferred']} | seniority={bd['seniority']} | edu={bd['education']}")

    print("="*70)


# ─────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Job–Resume Matching Engine")
    parser.add_argument("--jd", required=True, help="Job description file or text")
    parser.add_argument("--resumes-dir", default="./resumes")
    parser.add_argument("--persist-dir", default="./chroma_db")
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--output-json", default=None, help="Save results to JSON file")
    parser.add_argument("--no-filter", action="store_true", help="Disable hard filters")
    args = parser.parse_args()

    # Build or load index
    logger.info("Loading/building index from %s...", args.resumes_dir)
    collection, meta_store = build_rag_index(
        resumes_dir=args.resumes_dir,
        persist_dir=args.persist_dir,
    )
    logger.info("Index loaded: %d chunks, %d resumes", collection.count(), len(meta_store))

    # Load JD
    jd_path = Path(args.jd)
    if jd_path.exists():
        jd_text = jd_path.read_text()
    else:
        jd_text = args.jd  # treat as raw text

    # Match
    results = match_jobs(
        jd_text=jd_text,
        collection=collection,
        metadata_store=meta_store,
        top_k=args.top_k,
        apply_hard_filters=not args.no_filter,
    )

    print_results(results, verbose=True)

    if args.output_json:
        with open(args.output_json, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to {args.output_json}")
