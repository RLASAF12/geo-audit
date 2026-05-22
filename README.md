# geo-audit

> Score any web page for LLM visibility in 5 seconds. No installs, no API keys, pure Python.

---

## What it is

A CLI tool that fetches a URL and runs a **20-point GEO (Generative Engine Optimization) audit** — the checks that determine whether ChatGPT, Perplexity, Gemini, and Claude will cite your page in their answers.

## Why it exists

Traditional SEO tools optimize for ranking algorithms. GEO is different: AI search engines decide what to *cite* and *summarize* based on entity clarity, structured data, and citation-friendliness — not keyword density. This tool makes those signals visible.

## What's inside

```
geo-audit.py     — the entire tool (stdlib only, ~200 lines)
```

## Quick start

```bash
# Audit any URL
python3 geo-audit.py https://yoursite.com

# Machine-readable output
python3 geo-audit.py https://yoursite.com --json
```

**Example output:**
```
# GEO Audit Report: https://example.com
**AI SEARCH VERDICT:** The page demonstrates D-grade optimization.

## Audit Scores
⚠️ Entity Clarity:           3/5
❌ Citation-friendliness:    0/5
❌ Structure for extraction:  1/5
❌ Structured data coverage:  0/5

TOTAL SCORE: 4/20 | GRADE: F

## Recommended Fixes
- Entity: Ensure H1 matches Page Title and Meta Description for topic reinforcement.
- Citation: Add specific data points, dates, or author attribution to build trust signals.
- Structure: Use nested H2-H3 tags to create a query-responsive outline.
- Schema: Implement JSON-LD (Article, FAQ, or Product) to help LLMs parse your metadata.
```

## The 4 dimensions scored

| Dimension | Max | What it measures |
|-----------|-----|-----------------|
| Entity Clarity | /5 | Clear topic, matching H1 + title + meta description |
| Citation-friendliness | /5 | Stats, dates, author attribution, source signals |
| Structure for extraction | /5 | H2/H3 hierarchy that creates answer-ready chunks |
| Structured data coverage | /5 | JSON-LD schema (Article, FAQ, HowTo, Product) |

**Grading:** A (17–20) · B (14–16) · C (11–13) · D (8–10) · F (<8)

## Requirements

- Python 3.6+
- No pip installs — zero dependencies

---

Built by [Ben](https://github.com/RLASAF12) · nightly prototype loop · 2026-05-22
