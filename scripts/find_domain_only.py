#!/usr/bin/env python3
"""Scan references.bib for entries with domain-only URLs.

A domain-only URL has an empty path or just '/'.
Examples: https://arxiv.org, https://medium.com/, https://www.ibm.com
"""
import re
from pathlib import Path

BIB = Path(__file__).resolve().parent.parent / "references.bib"

ENTRY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)


def split_entries(text: str):
    out = []
    matches = list(ENTRY_RE.finditer(text))
    for i, m in enumerate(matches):
        key = m.group(1)
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out.append((key, text[start:end]))
    return out


def field(body: str, name: str):
    m = re.search(rf"\b{name}\s*=\s*[{{\"]", body, re.IGNORECASE)
    if not m:
        return None
    start = m.end() - 1
    open_ch = body[start]
    close_ch = "}" if open_ch == "{" else '"'
    depth = 1
    j = start + 1
    while j < len(body) and depth > 0:
        ch = body[j]
        if open_ch == "{":
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return body[start + 1 : j]
        else:
            if ch == close_ch:
                depth -= 1
                if depth == 0:
                    return body[start + 1 : j]
        j += 1
    return None


def is_domain_only(url: str) -> bool:
    if not url:
        return False
    u = url.strip()
    m = re.match(r"https?://([^/\s]+)(/?[^\s?#]*)", u)
    if not m:
        return False
    path = m.group(2) or ""
    return path in ("", "/")


def main():
    text = BIB.read_text()
    entries = split_entries(text)
    domain_only = []
    for key, body in entries:
        url = field(body, "url") or field(body, "howpublished")
        if url and is_domain_only(url):
            title = (field(body, "title") or "").replace("\n", " ").strip()
            author = (field(body, "author") or "").replace("\n", " ").strip()
            domain_only.append((key, url.strip(), title, author))
    print(f"Found {len(domain_only)} entries with domain-only URLs:\n")
    for key, url, title, author in domain_only:
        print(f"- {key}")
        print(f"    url:    {url}")
        print(f"    title:  {title[:100]}")
        print(f"    author: {author[:80]}")


if __name__ == "__main__":
    main()
