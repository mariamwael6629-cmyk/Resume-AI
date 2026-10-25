# Product

<!-- impeccable:product-schema 1 -->

> Inferred from the README, MIGRATION.md and `resume_ai.html`. The owner asked the redesign to proceed on inferred context; treat each line as an assumption until confirmed.

## Platform

web

## Users
Job seekers, often mid-search and anxious, checking whether their resume will get past automated screening. Some are career changers; some read Arabic. They come back between applications.

## Product Purpose
ResumeAI scores a resume against ATS rules (found and missing keywords, suggestions), matches seeded job listings by percentage, offers a resume builder that saves drafts, a dashboard of analyses and applications, and an admin panel. EN/AR toggle and light/dark theme.

## Positioning
It reads your resume the way a screener does and tells you what to fix.

## Capabilities and Constraints
- Single `resume_ai.html` (inline CSS/JS, Font Awesome icons), FastAPI + SQLite backend with JWT.
- Scoring and matching are deterministic keyword heuristics, not ML (see MIGRATION.md). Text input only; PDF/DOCX parsing is not implemented.

## Brand Commitments
- Name "ResumeAI".

## Evidence on Hand
- Landing stats, testimonials, FAQ claims (500+ ATS systems, AES-256, PDF/OCR support) and prices are placeholder marketing copy and some contradict MIGRATION.md. Do not add more; flag to the owner.

## Product Principles
1. Show the fix, not just the score.
2. Calm under stress: plain words, no hype.
3. Works the same in English and Arabic.
