#!/usr/bin/env python3
"""Search the locally installed Michael大麦哥 source corpus."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys


SKILL_ROOT = Path(__file__).resolve().parent.parent
CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
TRANSCRIPT_SKILL = Path(
    os.environ.get(
        "MICHAEL_DAMAI_TRANSCRIPT_DIR",
        CODEX_HOME / "skills" / "feiyuaq-michael-damaige",
    )
)
METADATA_SKILL = Path(
    os.environ.get(
        "MICHAEL_DAMAI_METADATA_DIR",
        CODEX_HOME / "skills" / "qwer-michael-damaige",
    )
)
GALLERY_CATALOG = Path(
    os.environ.get(
        "MICHAEL_DAMAI_GALLERY_CATALOG",
        CODEX_HOME / "skills" / "michael-damaige-gallery" / "public" / "catalog.json",
    )
)

PUNCTUATION = re.compile(
    r"[\s，。！？：；、,.!?;:（）()【】\[\]{}“”\"'`~@#$%^&*+=/\\|<>《》—-]+"
)
CHINESE_RUN = re.compile(r"[\u3400-\u9fff]+")
ASCII_TOKEN = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def terms_for(query: str) -> list[str]:
    terms: set[str] = set()
    for piece in PUNCTUATION.split(query):
        piece = piece.strip().lower()
        if len(piece) >= 2:
            terms.add(piece)
    for run in CHINESE_RUN.findall(query):
        if len(run) == 1:
            terms.add(run)
        for size in (2, 3, 4):
            for index in range(max(0, len(run) - size + 1)):
                terms.add(run[index : index + size])
    for token in ASCII_TOKEN.findall(query.lower()):
        if len(token) >= 2:
            terms.add(token)
    return sorted(terms, key=lambda item: (-len(item), item))


def score_text(text: str, terms: list[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(term) * min(len(term), 4) for term in terms)


def search_transcripts(terms: list[str], limit: int) -> list[dict]:
    script = TRANSCRIPT_SKILL / "scripts" / "search.py"
    if not script.is_file():
        return []
    results: list[dict] = []
    seen: set[tuple[str, int, int]] = set()
    for term in terms[:8]:
        proc = subprocess.run(
            [sys.executable, str(script), term, "--limit", str(max(2, limit))],
            cwd=TRANSCRIPT_SKILL,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if proc.returncode != 0:
            continue
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            continue
        for item in payload.get("results", []):
            key = (
                str(item.get("video_id", "")),
                int(item.get("cue_start", -1)),
                int(item.get("cue_end", -1)),
            )
            if key in seen:
                continue
            seen.add(key)
            item["source_type"] = "verbatim_transcript"
            item["platform"] = "Douyin"
            results.append(item)
    results.sort(key=lambda item: float(item.get("score", 0)), reverse=True)
    return results[:limit]


def search_gallery(terms: list[str], limit: int) -> list[dict]:
    if not GALLERY_CATALOG.is_file():
        return []
    catalog = load_json(GALLERY_CATALOG)
    candidates: list[dict] = []
    for video in catalog.get("videos", []):
        title = str(video.get("title", ""))
        title_score = score_text(title, terms) * 3
        excerpts = []
        for image in video.get("images", []):
            text = str(image.get("text", ""))
            score = title_score + score_text(text, terms)
            if score <= 0:
                continue
            excerpts.append(
                {
                    "id": image.get("id"),
                    "text": text,
                    "start_seconds": image.get("start"),
                    "score": score,
                }
            )
        if not excerpts:
            continue
        excerpts.sort(key=lambda item: item["score"], reverse=True)
        candidates.append(
            {
                "source_type": "timestamped_excerpt",
                "platform": "Bilibili",
                "bvid": video.get("bvid"),
                "title": title,
                "source_url": video.get("source"),
                "approval": video.get("approval"),
                "score": title_score + sum(item["score"] for item in excerpts[:2]),
                "excerpts": excerpts[:2],
            }
        )
    candidates.sort(key=lambda item: item["score"], reverse=True)
    return candidates[:limit]


def parse_metadata_sections(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig")
    matches = list(re.finditer(r"(?m)^## 视频 \d+｜(.+)$", text))
    sections: list[dict] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        title = match.group(1).strip()
        link_match = re.search(r"- 链接:\s*(\S+)", body)
        date_match = re.search(r"- 发布时间:\s*(.+)", body)
        sections.append(
            {
                "title": title,
                "body": body,
                "douyin_url": link_match.group(1) if link_match else None,
                "publication_date": date_match.group(1).strip() if date_match else None,
            }
        )
    return sections


def search_metadata(terms: list[str], limit: int) -> list[dict]:
    candidates = list(METADATA_SKILL.glob("kb/*.md"))
    if not candidates:
        return []
    results: list[dict] = []
    for path in candidates:
        for section in parse_metadata_sections(path):
            score = score_text(section["title"], terms) * 3 + score_text(
                section["body"], terms
            )
            if score <= 0:
                continue
            results.append(
                {
                    "source_type": "publisher_copy",
                    "platform": "Douyin",
                    "title": section["title"],
                    "source_url": section["douyin_url"],
                    "publication_date": section["publication_date"],
                    "score": score,
                    "content": section["body"],
                }
            )
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument(
        "--source",
        default="transcript,gallery,metadata",
        help="Comma-separated: transcript,gallery,metadata",
    )
    args = parser.parse_args()
    terms = terms_for(args.query)
    sources = {item.strip() for item in args.source.split(",") if item.strip()}
    availability = {
        "transcript": (TRANSCRIPT_SKILL / "scripts" / "search.py").is_file(),
        "gallery": GALLERY_CATALOG.is_file(),
        "metadata": bool(list(METADATA_SKILL.glob("kb/*.md"))),
    }
    output = {
        "query": args.query,
        "terms": terms[:20],
        "coverage": {
            "verbatim_transcripts": 19,
            "timestamped_excerpt_videos": 121,
            "publisher_copy_posts": 39,
            "unique_long_form_titles": 135,
            "douyin_profile_works": 209,
        },
        "source_available": availability,
        "results": [],
        "note": "Lexical candidates only. Read source context and cite titles/times; coverage is not the full 209-work profile.",
    }
    if "transcript" in sources:
        output["results"].extend(search_transcripts(terms, args.limit))
    if "gallery" in sources:
        output["results"].extend(search_gallery(terms, args.limit))
    if "metadata" in sources:
        output["results"].extend(search_metadata(terms, args.limit))
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
