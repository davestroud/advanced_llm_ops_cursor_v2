#!/usr/bin/env python3
"""Heuristic detector for prose passages that may need a citation.

Strategy: scan each chapter line-by-line, ignore non-prose environments,
and flag lines that contain a "needs-cite" signal AND have no \cite{}
within +/- 2 lines of context.

Signals:
  N  numeric/statistical claim with units or %
  P  attribution phrase ("studies show", "research suggests", ...)
  T  named technique/model/standard
  Q  direct quote (smart-quote pair around 30+ chars)

Output: docs/audit_reports/uncited_claims/<chapter>.md

The detector is INTENTIONALLY noisy. The author triages results.
False positives are acceptable; missed claims are not.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

OUT_DIR = Path("docs/audit_reports/uncited_claims")

NON_PROSE_ENVS = {
    "figure", "table", "tabular", "codebox", "minted",
    "llmalgobox", "llmlistingbox", "tikzpicture", "axis",
    "lstlisting", "equation", "align", "verbatim", "svgraybox",
    "epigraph", "center", "comment", "algorithm", "algorithmic",
    "longtable", "tabularx", "xltabular", "threeparttable",
}

ENV_BEGIN_RE = re.compile(r"\\begin\{(\w+)\*?\}")
ENV_END_RE = re.compile(r"\\end\{(\w+)\*?\}")
CITE_RE = re.compile(r"\\cite[a-z]*\{")

# attribution / hedge phrases that usually demand attribution
ATTRIB_RE = re.compile(
    r"(?i)\b("
    r"studies show|"
    r"research (shows?|suggests?|indicates?|finds?|demonstrates?)|"
    r"according to|"
    r"prior work|"
    r"recent (work|studies|research)|"
    r"the literature (shows?|reports?)|"
    r"surveys? (show|find|indicate)|"
    r"empirical(ly)? (shows?|demonstrates?|results?)|"
    r"benchmarks? (show|find|report|indicate)|"
    r"reportedly|"
    r"reports? (show|indicate|find)|"
    r"widely (reported|documented|known)|"
    r"has been (shown|demonstrated|reported|observed)|"
    r"industry reports?|"
    r"practitioners report|"
    r"engineers report|"
    r"as (shown|demonstrated|reported) in|"
    r"a study (by|of|from)|"
    r"a survey (of|by)"
    r")\b"
)

# named techniques / models / standards we consider third-party
NAMED_TERMS = [
    "FlashAttention", "PagedAttention", "SmoothQuant", "GPTQ", r"\bAWQ\b",
    "LoRA", "QLoRA", "RLHF", r"\bDPO\b", "InstructGPT", r"GPT-?[34](\.[0-9])?",
    "GPT-4o", r"Claude\s?[34]", r"Llama-?[23]", "Mistral", "Mixtral",
    "Falcon", "Gemma", r"Phi-?[234]", r"\bPaLM\b", "Gemini", "BLOOM",
    r"\bOPT\b", "Mixture of Experts", "FlashInfer", r"\bvLLM\b",
    "TensorRT-LLM", "TensorRT", r"\bSGLang\b", r"\bTGI\b", "MLPerf",
    r"\bHELM\b", "MT-Bench", "AlpacaEval", "TruthfulQA", r"\bMMLU\b",
    "HumanEval", "BIG-bench", r"\bGLUE\b", "SuperGLUE", r"\bSQuAD\b",
    "GSM8K", "HotpotQA", "TriviaQA", "Natural Questions", "MS MARCO",
    r"\bBEIR\b", r"\bFAISS\b", "Milvus", "Pinecone", "Weaviate", "Chroma",
    "Qdrant", "LangChain", "LangGraph", "LangSmith", "LlamaIndex",
    "Semantic Kernel", "AutoGen", "CrewAI", "Temporal", r"\bRay\b",
    "Kubernetes", r"H100\b", r"A100\b", r"H200\b", r"B200\b", r"GB200\b",
    r"TPU\s?v[0-9]+", r"\bGDPR\b", r"\bCCPA\b", r"\bHIPAA\b", r"SOC ?2",
    "ISO ?27001", "NIST AI RMF", "EU AI Act", "OECD AI", "Schrems II",
    r"\bRAG\b", "RAGAS", "Constitutional AI", "Tree of Thoughts",
    r"Chain[- ]of[- ]Thought", r"\bReAct\b", "Reflexion", "Toolformer",
    "FrugalGPT", "Self-Refine",
]
NAMED_RE = re.compile("|".join(NAMED_TERMS))

# numeric-claim signal: percent, x-fold, money, latency/throughput units
NUMERIC_RE = re.compile(
    r"(?<![\\\$_a-zA-Z])"  # not part of a LaTeX command, escape, or word
    r"(?:[0-9]+(?:\.[0-9]+)?)"
    r"\s?"
    r"(?:%"
    r"|(?:x|×|-fold)"
    r"|(?:ms|s\b|min\b|hours?|seconds?|milliseconds?)"
    r"|(?:tokens?/s|TPS\b|QPS\b|RPS\b)"
    r"|(?:GB|MB|KB|TB|GiB|MiB|TiB)"
    r"|(?:FLOPS?|FLOPs|TFLOPS?|PFLOPS?)"
    r"|(?:billion|trillion|million)"
    r"|(?:param(?:eter)?s?\b)"
    r")"
    r"|(?:\$[0-9]+(?:\.[0-9]+)?[MBK]?)"
)

# direct-quote dumb match: matched smart quotes, 30+ chars between
QUOTE_RE = re.compile(r"[\u201C\u201E\u2018\u201A][^\u201D\u2019]{30,}[\u201D\u2019]")

# lines we always skip (commands-only, headings, bookkeeping)
SKIP_LINE_PATTERNS = [
    re.compile(r"^\s*\\(chapter|section|subsection|subsubsection|paragraph)\*?\{"),
    re.compile(r"^\s*\\(label|input|include|caption|index|emph|textbf|textit)\{"),
    re.compile(r"^\s*\\(begin|end)\{"),
    re.compile(r"^\s*%"),
    re.compile(r"^\s*$"),
    re.compile(r"^\s*\\printbibliography"),
    re.compile(r"^\s*\\noindent\\textbf\{Chapter roadmap"),
    re.compile(r"^\s*\\(BestPracticeBox|PitfallBox|DefinitionBox|ChecklistBox|IshtarVignette|llm[a-z]*box)"),
    re.compile(r"^\s*\\item\s*$"),
]


def scan_file(path: Path) -> tuple[list[str], int]:
    """Returns (markdown_lines, total_hits)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    env_depth = 0
    env_stack: list[str] = []
    hits: list[tuple[int, str, str]] = []  # (line_no, signals, snippet)

    cite_lines = set()
    for i, line in enumerate(lines, start=1):
        if CITE_RE.search(line):
            cite_lines.add(i)

    for i, line in enumerate(lines, start=1):
        # update env depth
        for m in ENV_BEGIN_RE.finditer(line):
            if m.group(1) in NON_PROSE_ENVS:
                env_stack.append(m.group(1))
        for m in ENV_END_RE.finditer(line):
            if env_stack and m.group(1) == env_stack[-1]:
                env_stack.pop()
        env_depth = len(env_stack)

        if env_depth > 0:
            continue

        if any(p.match(line) for p in SKIP_LINE_PATTERNS):
            continue

        # check ±2 lines for an existing \cite
        if any((i + d) in cite_lines for d in (-2, -1, 0, 1, 2)):
            continue

        sigs = ""
        if ATTRIB_RE.search(line):
            sigs += "P"
        if NAMED_RE.search(line):
            sigs += "T"
        if NUMERIC_RE.search(line):
            sigs += "N"
        if QUOTE_RE.search(line):
            sigs += "Q"

        if not sigs:
            continue

        snippet = " ".join(line.split())
        if len(snippet) > 220:
            snippet = snippet[:217] + "..."
        hits.append((i, sigs, snippet))

    md = [
        f"# Uncited claims — {path.name}",
        "",
        "_Heuristic scan; expect false positives. Triage with the author._",
        "",
        "Legend: N=numeric P=attribution T=named-technique Q=direct-quote",
        "",
        "---",
        "",
    ]
    for line_no, sigs, snippet in hits:
        md.append(f"- L{line_no:<5} [{sigs:<4}] {snippet}")
    md += ["", "---", "", f"**Total candidate lines:** {len(hits)}", ""]

    return md, len(hits)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    chapters = sorted(Path(".").glob("ch*.tex"))
    summary = []
    for ch in chapters:
        out_path = OUT_DIR / (ch.stem + ".md")
        md, hits = scan_file(ch)
        out_path.write_text("\n".join(md), encoding="utf-8")
        summary.append((ch.name, hits, str(out_path)))
        print(f"{ch.name:<32} {hits:4d} candidate lines -> {out_path}")

    summary_path = OUT_DIR / "_summary.md"
    lines = [
        "# Uncited-claims summary",
        "",
        "| Chapter | Candidate lines | Report |",
        "|---|---:|---|",
    ]
    for name, hits, path in summary:
        lines.append(f"| {name} | {hits} | [{path}]({path.split('/',2)[-1]}) |")
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nSummary -> {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
