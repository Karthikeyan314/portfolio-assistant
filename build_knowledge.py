"""Build the assistant's knowledge base: profile notes plus public project docs.

Sources:
    knowledge/profile/*.md      hand-written professional profile (public-safe)
    knowledge/projects.yaml     public GitHub projects and the doc files to learn from
    knowledge/projects/<name>/  snapshots of those files (committed, so builds are offline)

    python build_knowledge.py            # rebuild knowledge/chunks.jsonl from snapshots
    python build_knowledge.py --refresh  # download fresh project snapshots first

Every chunk records a source label and a link, so answers can cite them. The build fails
if any chunk looks like private data (phone numbers, email addresses, internal markers),
because the knowledge base is published with a public Space.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
KNOWLEDGE = ROOT / "knowledge"
OUT = KNOWLEDGE / "chunks.jsonl"
SELF_REPO = "Karthikeyan314/portfolio-assistant"
MAX_CHARS = 1800

# Anything matching these must never reach the public knowledge base.
PRIVATE_PATTERNS = {
    "phone number": re.compile(r"(?<![\w/-])\+?\d[\d \-]{9,}\d(?![\w/-])"),
    "email address": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "internal marker": re.compile(
        r"confidential|internal use|prepared for|scratch_book|coo-cs|\.mcs\.yml|"
        r"self[- ]review|work_log|dev\\|prod\\",
        re.I,
    ),
}


def load_projects() -> list[dict]:
    return yaml.safe_load((KNOWLEDGE / "projects.yaml").read_text(encoding="utf-8"))["projects"]


def refresh_snapshots(projects: list[dict]) -> None:
    for p in projects:
        for rel in p["files"]:
            url = f"https://raw.githubusercontent.com/{p['repo']}/{p['branch']}/{rel}"
            dest = KNOWLEDGE / "projects" / p["name"] / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(url, timeout=30) as resp:  # noqa: S310 (fixed host)
                dest.write_bytes(resp.read())
            print(f"downloaded {p['repo']}/{rel}")


def chunk_markdown(text: str, source: str, url: str, prefix: str = "") -> list[dict]:
    """Split Markdown on #, ## and ### headings; long sections split on paragraphs."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)  # Space front matter
    text = re.sub(r"```mermaid.*?```", "", text, flags=re.S)  # diagrams read as noise
    chunks, heading, buf = [], prefix.rstrip(": ") or source, []
    for line in text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.*)", line)
        if m and buf:
            chunks += _flush(heading, "\n".join(buf), source, url)
            buf = []
        if m:
            heading = f"{prefix}{m.group(2)}"
        buf.append(line)
    if buf:
        chunks += _flush(heading, "\n".join(buf), source, url)
    return chunks


def _flush(title: str, body: str, source: str, url: str) -> list[dict]:
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S).strip()
    if len(body) < 40 or "TODO:" in body:
        return []
    parts, cur = [], ""
    for para in body.split("\n\n"):
        if cur and len(cur) + len(para) > MAX_CHARS:
            parts.append(cur)
            cur = ""
        cur = f"{cur}\n\n{para}" if cur else para
    parts.append(cur)
    return [{"title": title, "source": source, "url": url, "text": p.strip()} for p in parts]


def projects_overview(projects: list[dict]) -> dict:
    lines = ["Karthikeyan's public portfolio projects on GitHub:"]
    for p in projects:
        lines.append(
            f"- {p['title']} (https://github.com/{p['repo']}): {' '.join(p['summary'].split())} "
            f"Skills shown: {', '.join(p['skills'])}."
        )
    return {
        "title": "Portfolio projects overview",
        "source": "projects.yaml",
        "url": f"https://github.com/{SELF_REPO}/blob/main/knowledge/projects.yaml",
        "text": "\n".join(lines),
    }


def build(projects: list[dict]) -> list[dict]:
    chunks = []
    for md in sorted((KNOWLEDGE / "profile").glob("*.md")):
        label = f"profile/{md.stem.split('_', 1)[-1]}"
        url = f"https://github.com/{SELF_REPO}/blob/main/knowledge/profile/{md.name}"
        chunks += chunk_markdown(md.read_text(encoding="utf-8"), label, url)
    chunks.append(projects_overview(projects))
    for p in projects:
        for rel in p["files"]:
            path = KNOWLEDGE / "projects" / p["name"] / rel
            url = f"https://github.com/{p['repo']}/blob/{p['branch']}/{rel}"
            chunks += chunk_markdown(
                path.read_text(encoding="utf-8"), f"{p['name']}/{rel}", url, f"{p['title']}: "
            )
    for i, c in enumerate(chunks):
        c["id"] = i
    return chunks


def privacy_violations(chunks: list[dict]) -> list[str]:
    found = []
    for c in chunks:
        for label, pattern in PRIVATE_PATTERNS.items():
            if m := pattern.search(f"{c['title']}\n{c['text']}"):
                found.append(f"{c['source']} / {c['title']}: {label} ({m.group(0)!r})")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--refresh", action="store_true", help="download project snapshots")
    args = parser.parse_args()
    projects = load_projects()
    if args.refresh:
        refresh_snapshots(projects)
    chunks = build(projects)
    if problems := privacy_violations(chunks):
        print("Refusing to write the knowledge base; private-looking content found:")
        print("\n".join(f"  {p}" for p in problems))
        return 1
    OUT.write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in chunks) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {len(chunks)} chunks to {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
