"""
GEO-AUDIT CLI - Production-quality Generative Engine Optimization Auditor
Sample Run:
$ python3 geo-audit.py https://example.com
# GEO Audit Report: https://example.com
AI SEARCH VERDICT: The page provides a clear baseline entity but lacks the structured
depth required for high-confidence AI synthesis. Strengthening citation signals and
expanding JSON-LD would significantly improve visibility in generative summaries.

## Audit Scores
✅ Entity Clarity: 4/5
⚠️ Citation-friendliness: 2/5
⚠️ Structure for extraction: 3/5
❌ Structured data coverage: 0/5

TOTAL SCORE: 9/20 | GRADE: D
...
"""

import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser
import json
import re
import sys
import argparse

class GeoParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {"title": "", "meta": {}, "headings": {"h1": [], "h2": [], "h3": []},
                     "json_ld": [], "canonical": "", "text_content": [], "link_words": 0}
        self.current_tag = None
        self.in_script = False
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        if tag == "meta":
            name = attrs_dict.get("name") or attrs_dict.get("property")
            if name: self.data["meta"][name.lower()] = attrs_dict.get("content", "")
        elif tag == "link" and attrs_dict.get("rel") == "canonical":
            self.data["canonical"] = attrs_dict.get("href", "")
        elif tag in self.data["headings"]:
            self.current_tag = tag
        elif tag == "script" and attrs_dict.get("type") == "application/ld+json":
            self.in_script = "jsonld"
        elif tag in ["script", "style"]:
            self.in_style = True

    def handle_endtag(self, tag):
        if tag in ["script", "style"]: self.in_style = False; self.in_script = False
        self.current_tag = None

    def handle_data(self, data):
        if self.in_style or (self.in_script and self.in_script != "jsonld"): return
        clean_data = data.strip()
        if not clean_data: return

        if self.in_script == "jsonld":
            try: self.data["json_ld"].append(json.loads(clean_data))
            except: pass
        elif self.current_tag == "title": self.data["title"] = clean_data
        elif self.current_tag in self.data["headings"]: self.data["headings"][self.current_tag].append(clean_data)

        self.data["text_content"].append(clean_data)
        if self.current_tag == "a": self.data["link_words"] += len(clean_data.split())

def audit_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GeoAudit/1.0"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")
            final_url = response.geturl()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        sys.exit(1)

    parser = GeoParser()
    parser.feed(html)
    d = parser.data
    full_text = " ".join(d["text_content"])
    word_count = len(full_text.split())

    # Audit Logic
    scores = {"Entity": 0, "Citation": 0, "Structure": 0, "Schema": 0}
    fixes = []

    # 1. Entity Clarity
    if d["title"]: scores["Entity"] += 1
    if d["headings"]["h1"]: scores["Entity"] += 2
    if d["meta"].get("description"): scores["Entity"] += 2
    if scores["Entity"] < 4: fixes.append("Entity: Ensure H1 matches Page Title and Meta Description for topic reinforcement.")

    # 2. Citation-friendliness
    if re.search(r"\d{4}", full_text): scores["Citation"] += 1 # Dates
    if re.search(r"(\d+%|\d+\.\d+)", full_text): scores["Citation"] += 2 # Stats
    if any(k in full_text.lower() for k in ["source", "author", "published", "according to"]): scores["Citation"] += 2
    if scores["Citation"] < 3: fixes.append("Citation: Add specific data points, dates, or author attribution to build trust signals.")

    # 3. Structure
    if d["headings"]["h1"]: scores["Structure"] += 1
    if len(d["headings"]["h2"]) >= 2: scores["Structure"] += 2
    if len(d["headings"]["h3"]) >= 1: scores["Structure"] += 2
    if scores["Structure"] < 4: fixes.append("Structure: Use nested H2-H3 tags to create a query-responsive outline.")

    # 4. Schema
    if d["json_ld"]:
        scores["Schema"] = 5
    else:
        fixes.append("Schema: Implement JSON-LD (Article, FAQ, or Product) to help LLMs parse your metadata.")

    total = sum(scores.values())
    grade = "F"
    if total >= 17: grade = "A"
    elif total >= 14: grade = "B"
    elif total >= 11: grade = "C"
    elif total >= 8: grade = "D"

    report = {
        "url": final_url, "word_count": word_count, "link_density": round(d["link_words"]/max(1, word_count), 2),
        "scores": scores, "total": total, "grade": grade, "fixes": fixes,
        "verdict": f"The page demonstrates {grade}-grade optimization. " +
                   ("High extraction potential." if total > 15 else "Requires structural refinement to anchor in AI latent space.")
    }
    return report

def print_markdown(r):
    def emo(s): return "✅" if s >= 4 else "⚠️" if s >= 2 else "❌"
    print(f"# GEO Audit Report: {r['url']}")
    print(f"**AI SEARCH VERDICT:** {r['verdict']}\n")
    print("## Audit Scores")
    print(f"{emo(r['scores']['Entity'])} Entity Clarity: {r['scores']['Entity']}/5")
    print(f"{emo(r['scores']['Citation'])} Citation-friendliness: {r['scores']['Citation']}/5")
    print(f"{emo(r['scores']['Structure'])} Structure for extraction: {r['scores']['Structure']}/5")
    print(f"{emo(r['scores']['Schema'])} Structured data coverage: {r['scores']['Schema']}/5\n")
    print(f"**TOTAL SCORE: {r['total']}/20 | GRADE: {r['grade']}**\n")
    if r['fixes']:
        print("## Recommended Fixes")
        for f in r['fixes']: print(f"- {f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GEO Audit CLI")
    parser.add_argument("url", help="Target URL to audit")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    res = audit_url(args.url)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print_markdown(res)
