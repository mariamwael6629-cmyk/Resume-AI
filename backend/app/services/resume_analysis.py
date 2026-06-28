"""
HEURISTIC STUB: This module does NOT use real ML/NLP/OCR.
It is a deterministic, keyword-and-length-based heuristic that stands in for
a future real ATS-scoring / resume-parsing model. All "scores" are computed
from simple string matching so that the demo is consistent and explainable,
not because any AI model produced them.
"""

import re

# Keyword categories used purely for deterministic scoring/demo purposes.
HIGH_VALUE_KEYWORDS = [
    "python", "javascript", "typescript", "react", "node.js", "node",
    "sql", "aws", "docker", "kubernetes", "graphql", "ci/cd", "git",
    "rest api", "agile", "machine learning", "java", "c++", "go",
    "html", "css", "next.js", "vue", "angular", "azure", "gcp",
]

ACTION_VERBS = [
    "led", "built", "developed", "implemented", "designed", "launched",
    "improved", "optimized", "created", "managed", "architected",
    "increased", "reduced", "mentored", "delivered", "automated",
]

METRIC_PATTERN = re.compile(r"\b\d+(\.\d+)?\s?(%|percent|x|k|m|million|hours|days|users)\b", re.IGNORECASE)


def _clamp(value: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, value))


def analyze_resume_text(text: str, filename: str = "") -> dict:
    """
    HEURISTIC STUB — deterministic scoring, not a real ML model.

    Derives plausible ATS sub-scores and suggestions from:
      - text length (proxy for "completeness")
      - presence of known high-value keywords
      - presence of action verbs
      - presence of quantified metrics (e.g. "40%", "2x", "10 hours")
      - file extension (PDF/DOCX assumed more ATS-friendly than others)
    """
    text_lower = (text or "").lower()
    word_count = len(text_lower.split())

    found_keywords = sorted({kw for kw in HIGH_VALUE_KEYWORDS if kw in text_lower})
    missing_keywords = sorted(set(HIGH_VALUE_KEYWORDS) - set(found_keywords))[:8]

    found_verbs = [v for v in ACTION_VERBS if v in text_lower]
    metric_hits = len(METRIC_PATTERN.findall(text_lower))

    # Formatting score: based on file type + reasonable length
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    formatting_score = 70
    if ext in ("pdf", "docx", "doc"):
        formatting_score += 15
    if 150 <= word_count <= 1200:
        formatting_score += 10
    formatting_score = _clamp(formatting_score)

    # Keyword score: scaled by fraction of high-value keywords found
    keyword_ratio = len(found_keywords) / max(len(HIGH_VALUE_KEYWORDS), 1)
    keywords_score = _clamp(int(40 + keyword_ratio * 120))

    # Experience score: based on action verbs + quantified metrics present
    experience_score = _clamp(int(50 + len(found_verbs) * 4 + metric_hits * 6))

    # Education score: presence of common education terms
    education_terms = ["bachelor", "master", "b.sc", "m.sc", "phd", "university", "college", "degree"]
    education_hits = sum(1 for t in education_terms if t in text_lower)
    education_score = _clamp(60 + education_hits * 10)

    ats_score = _clamp(
        round(
            formatting_score * 0.25
            + keywords_score * 0.30
            + experience_score * 0.30
            + education_score * 0.15
        )
    )

    suggestions = []
    if metric_hits == 0:
        suggestions.append(
            "Add quantified achievements (e.g. \"reduced load time by 40%\") to strengthen impact statements."
        )
    if len(found_verbs) < 3:
        suggestions.append(
            "Use more strong action verbs (e.g. \"led\", \"built\", \"optimized\") at the start of bullet points."
        )
    if len(missing_keywords) > 0:
        suggestions.append(
            f"Consider adding relevant keywords such as: {', '.join(missing_keywords[:5])}."
        )
    if word_count < 150:
        suggestions.append("Your resume looks short — consider expanding on your experience and projects.")
    if word_count > 1200:
        suggestions.append("Your resume is quite long — consider trimming to focus on the most relevant experience.")
    if not suggestions:
        suggestions.append("Great job! Your resume covers keywords, action verbs, and quantified results well.")

    return {
        "ats_score": ats_score,
        "formatting_score": formatting_score,
        "keywords_score": keywords_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "found_keywords": found_keywords[:12] or ["general experience"],
        "missing_keywords": missing_keywords,
        "suggestions": suggestions,
    }
