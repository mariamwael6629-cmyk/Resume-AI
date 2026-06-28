"""
HEURISTIC STUB: This module does NOT use real ML-based job matching.
Match percentages are computed deterministically by comparing job tags /
description text against the keywords found in a user's most recent resume
analysis. This stands in for a future trained matching model.
"""


def compute_match_percent(job_tags: list[str], job_description: str, user_found_keywords: list[str]) -> int:
    """
    HEURISTIC STUB — deterministic overlap-based scoring, not ML.

    If the user has no resume on file, callers should treat match_percent as
    None (no personalization) rather than calling this function.
    """
    if not user_found_keywords:
        return 60  # neutral baseline when no signal available

    haystack = " ".join(job_tags).lower() + " " + (job_description or "").lower()
    keywords = [k.lower() for k in user_found_keywords]
    hits = sum(1 for k in keywords if k in haystack)
    ratio = hits / max(len(keywords), 1)

    # Base of 55 so unrelated jobs still show a plausible (low-ish) number,
    # scaled up to 98 max for strong overlap.
    score = 55 + int(ratio * 43)
    return max(40, min(98, score))
