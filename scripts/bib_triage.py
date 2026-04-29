#!/usr/bin/env python3
"""Triage references.bib + chapter prose:

  1. Parse references.bib into structured entries (key, type, fields).
  2. Identify cited keys (across ch*.tex).
  3. Classify orphans:
     - PLACEHOLDER  : author contains 'Placeholder' / 'Name, Placeholder'
                      OR title contains 'arXiv:NNNN.xxxxx' patterns
     - DUPLICATE    : same DOI / similar title to a cited entry
     - SHOULD_CITE  : not cited, but its likely-named subject is mentioned
                      in chapter prose (heuristic name match)
     - REMOVABLE    : not cited and no obvious subject match in prose
  4. Build a candidate "class-A cite map":
     for each orphan that looks SHOULD_CITE, list each chapter+line where the
     subject name appears in prose (and no \cite{} sits within +/-2 lines).

Output: docs/audit_reports/bib_triage.md
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict

OUT_DIR = Path("docs/audit_reports")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "bib_triage.md"
DATA_FILE = OUT_DIR / "bib_triage.json"

CITE_RE = re.compile(r"\\cite[a-z]*\{([^}]+)\}")
ENV_BEGIN_RE = re.compile(r"\\begin\{(\w+)\*?\}")
ENV_END_RE = re.compile(r"\\end\{(\w+)\*?\}")
NON_PROSE_ENVS = {
    "figure", "table", "tabular", "codebox", "minted",
    "llmalgobox", "llmlistingbox", "tikzpicture", "axis",
    "lstlisting", "equation", "align", "verbatim", "svgraybox",
    "epigraph", "comment", "algorithm", "algorithmic",
    "longtable", "tabularx", "xltabular", "threeparttable",
}


def parse_bib(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    entries = {}
    i = 0
    while i < len(text):
        if text[i] != "@":
            i += 1
            continue
        # find type
        m = re.match(r"@(\w+)\{([^,]+),", text[i:])
        if not m:
            i += 1
            continue
        etype = m.group(1)
        key = m.group(2).strip()
        # find matching brace
        depth = 0
        j = i
        while j < len(text):
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = text[i:j+1]
        # extract fields
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*([\"\{])", body):
            field_name = fm.group(1).lower()
            opener = fm.group(2)
            close = "}" if opener == "{" else '"'
            start = fm.end()
            d = 1
            k = start
            while k < len(body):
                if body[k] == opener and opener == "{":
                    d += 1
                elif body[k] == close:
                    d -= 1
                    if d == 0:
                        fields[field_name] = body[start:k].strip()
                        break
                k += 1
        entries[key] = {"type": etype, "key": key, "fields": fields}
        i = j + 1
    return entries


def find_cited_keys(chapter_files: list[Path]) -> set:
    keys = set()
    for f in chapter_files:
        for m in CITE_RE.finditer(f.read_text(encoding="utf-8", errors="replace")):
            for k in m.group(1).split(","):
                keys.add(k.strip())
    return keys


def is_placeholder(entry: dict) -> bool:
    f = entry["fields"]
    text = " ".join(f.get(k, "") for k in ("author", "title", "journal", "url"))
    if re.search(r"\bPlaceholder\b", text):
        return True
    if re.search(r"\barxiv\.org\s*$", f.get("url", "").strip(), re.IGNORECASE):
        # arxiv with no ID is a smell, but only flag if author is 'Placeholder' too
        pass
    if re.search(r"arXiv:\s*\d{4}\.x{3,}", text):
        return True
    if re.search(r"^Author,\s*Placeholder", f.get("author", "")):
        return True
    if re.search(r"^Name,\s*Placeholder", f.get("author", "")):
        return True
    return False


def subject_terms(entry: dict) -> list[str]:
    """Extract likely 'subject' terms (tool/paper name) from a bib entry, used to
    grep for first-mention sites in chapter prose."""
    f = entry["fields"]
    terms: list[str] = []

    # explicit known mapping for tool docs / vendor pages
    KEY_MAP = {
        "vllm": [r"\bvLLM\b"],
        "vllm-paper": [r"\bvLLM\b", "PagedAttention"],
        "tgi": [r"\bTGI\b", "Text Generation Inference"],
        "tgi-whitepaper": [r"\bTGI\b", "Text Generation Inference"],
        "tensorrt-llm": ["TensorRT-LLM"],
        "tensorrt-llm-github": ["TensorRT-LLM"],
        "tensorrt2023": ["TensorRT"],
        "tensorrtllm": ["TensorRT-LLM"],
        "sglang2024": [r"\bSGLang\b"],
        "Zheng2023SGLang": [r"\bSGLang\b"],
        "Zheng2024sglang": [r"\bSGLang\b"],
        "faiss_blog": [r"\bFAISS\b"],
        "faiss_github": [r"\bFAISS\b"],
        "johnson2017billion": [r"\bFAISS\b"],
        "johnson2017faiss": [r"\bFAISS\b"],
        "Milvus2023": ["Milvus"],
        "Zilliz2023": ["Milvus", "Zilliz"],
        "pinecone_hybrid_docs": ["Pinecone"],
        "weaviate_hybrid_docs": ["Weaviate"],
        "langchain_retrievers_docs": ["LangChain"],
        "langchainDocs": ["LangChain"],
        "LangChain2023Framework": ["LangChain"],
        "llamaindex_rag_docs": ["LlamaIndex", "Llama Index"],
        "llamaindexDocs": ["LlamaIndex", "Llama Index"],
        "langfuse": ["LangFuse"],
        "langfuse_blog": ["LangFuse"],
        "langfuse_data_model": ["LangFuse"],
        "langfuse_docs": ["LangFuse"],
        "langfuse_eval_overview": ["LangFuse"],
        "langgraph_docs": ["LangGraph"],
        "langgraph_graph_api": ["LangGraph"],
        "langgraph_overview": ["LangGraph"],
        "LangGraph2024Framework": ["LangGraph"],
        "langsmith_docs": ["LangSmith"],
        "langsmith_eval_docs": ["LangSmith"],
        "langsmith_online_evals": ["LangSmith"],
        "langsmithDocs3": ["LangSmith"],
        "langsmithDocs4": ["LangSmith"],
        "CrewAI2024Framework": ["CrewAI"],
        "autogen": ["AutoGen"],
        "semantic_kernel_agent_orchestration": ["Semantic Kernel"],
        "temporal_workflow_execution": ["Temporal"],
        "temporal_workflows_docs": ["Temporal"],
        "toolformer": ["Toolformer"],
        "trulens2023": ["TruLens"],
        "openaievals": ["OpenAI Evals"],
        "wandb": [r"\bW&B\b", "Weights & Biases", "wandb"],
        "mlflow": ["MLflow"],
        "ragas": ["RAGAS"],
        "cloud2023ragas": ["RAGAS"],
        "cloud2023eval": [],
        "promptlayer": ["PromptLayer"],
        "agentbench2024": ["AgentBench"],
        "auditing_llms": [],
        "ccpa2018": [r"\bCCPA\b"],
        "gdpr2016": [r"\bGDPR\b"],
        "iso27001": ["ISO ?27001"],
        "soc2": [r"SOC ?2"],
        "oecd_ai_principles": ["OECD"],
        "schremsII2020": ["Schrems II", "Schrems-II"],
        "neuripshybrid2023": ["hybrid retrieval", "hybrid search"],
        "kvcompress2024": ["KV cache", "KV-cache compression"],
        "yan2025specdecoding": ["speculative decoding"],
        "Liu2023Scissorhands": ["Scissorhands"],
        "Guha2024Smoothie": ["Smoothie"],
        "smoothie2023": ["Smoothie"],
        "smoothie2024": ["Smoothie"],
        "model-cascade": ["model cascade", "cascading"],
        "FrugalGPT": ["FrugalGPT"],
        "Borzunov2023distributed": ["Petals", "distributed inference"],
        "Borzunov2023Petals": ["Petals"],
        "petals2023": ["Petals"],
        "Chowdhery2022palm": [r"\bPaLM\b"],
        "ouyang2022instructgpt": ["InstructGPT"],
        "bai2022constitutional": ["Constitutional AI"],
        "su2021rope": [r"\bRoPE\b", "rotary position"],
        "ner2023": ["named entity recognition"],
        "AICOM2023": [],
        "ai.stackexchange": [],
        "AIStackexchange2022Memory": [],
        "aimultipleEval2": [],
        "alabdulmohsin2023falcon": ["Falcon"],
        "analyticsindiamag2022a": [],
        "analyticsindiamag2022b": [],
        "arize": ["Arize"],
        "arize2": ["Arize"],
        "AWS2023NeuralSparse": [r"\bNeural Sparse\b"],
        "Author2024AWQ": [],  # placeholder, drop
        "Author2024NonDeterminism": [],  # placeholder
        "Name2022GalacticaCritique": [],  # placeholder
        "Placeholder2022GalacticaNote": [],  # placeholder
        "awq": [r"\bAWQ\b"],
        "awq_2023": [r"\bAWQ\b"],
        "gptq": [r"\bGPTQ\b"],
        "dettmers2022int8": ["LLM.int8", "int8"],
        "tpuv4paper": [r"TPU v4"],
        "megatron_lm_2019": ["Megatron-LM"],
        "mig2021": [r"\bMIG\b"],
        "skypilot2023": ["SkyPilot"],
        "zenml2023": ["ZenML"],
        "ZenML2023CharacterAI": ["Character.AI", "Character AI"],
        "huggingface_scaling2024": [],
        "circleci_hallucinations": ["CircleCI"],
        "Devto2023": [],
        "Reuters2023Bard": [r"\bBard\b"],
        "Team2023Sydney": ["Sydney", "Bing"],
        "vice2022": [],
        "theverge2022": [],
        "theverge2023": [],
        "ExplodingTopics2024GPT4": ["GPT-4"],
        "kamathDeepDive": [],
        "Ke4e1qarpukhin2020DPR": [r"\bDPR\b"],
        "Lewis2020RAGb": [r"\bRAG\b"],
        "neptune2023rag": [r"\bRAG\b"],
        "Vincent2022Galactica": ["Galactica"],
        "ibm2023": [r"\bIBM\b"],
        "graves2021": [],
        "stanfordcs336": [],
        "weidinger2021": [],
        "ward2020": [],
        "dawnbench2019": ["DawnBench"],
        "dawninfra2023": [],
        "thecloudplaybook1": [],
        "thecloudplaybook2": [],
        "cloudplaybook1": [],
        "cloudplaybook2": [],
        "Devto2023": [],
        "encoder-ops-2": [],
        "emergentmind3": [],
        "gallegos2024": [],
        "hopper2022": [r"\bH100\b"],
        "kvcompress2024": ["KV cache"],
        "langchain2025otel": ["LangChain", "OpenTelemetry"],
        "posthog2025observability": ["PostHog"],
        "promptlayer": ["PromptLayer"],
        "tensorrt2023": ["TensorRT"],
        "touvron2023llama": ["LLaMA"],
        "black2022gptneox": ["GPT-NeoX"],
        "bansal2025murf": ["MURF"],
        "Zhang2024Coupled": [],
    }
    if entry["key"] in KEY_MAP:
        terms.extend(KEY_MAP[entry["key"]])

    # also try title words (>=4 chars, capitalized)
    title = f.get("title", "")
    for w in re.findall(r"[A-Z][A-Za-z0-9-]{3,}", title):
        if w not in {"The", "This", "That", "From", "With", "Their", "These"}:
            terms.append(w)

    seen = set()
    out = []
    for t in terms:
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def find_first_mentions(term: str, chapter_files: list[Path]) -> list[tuple[Path, int, str]]:
    """Find first-mention prose lines (no \cite{} ±2 lines, not inside non-prose env)."""
    pat = re.compile(term)
    hits = []
    for f in chapter_files:
        text = f.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        cite_lines = {i for i, line in enumerate(lines, 1) if CITE_RE.search(line)}
        env_stack: list[str] = []
        for i, line in enumerate(lines, 1):
            for m in ENV_BEGIN_RE.finditer(line):
                if m.group(1) in NON_PROSE_ENVS:
                    env_stack.append(m.group(1))
            for m in ENV_END_RE.finditer(line):
                if env_stack and m.group(1) == env_stack[-1]:
                    env_stack.pop()
            if env_stack:
                continue
            if not pat.search(line):
                continue
            if any((i + d) in cite_lines for d in (-2, -1, 0, 1, 2)):
                continue
            hits.append((f, i, line.strip()))
            break  # first mention only
    return hits


def main() -> None:
    bib = parse_bib(Path("references.bib"))
    chapters = sorted(Path(".").glob("ch*.tex"))
    cited = find_cited_keys(chapters)

    classified = {
        "placeholder": [],
        "orphan_should_cite": [],
        "orphan_no_obvious_site": [],
        "cited_ok": [],
    }
    cite_map: dict[str, list] = {}

    for key, entry in bib.items():
        if key in cited:
            classified["cited_ok"].append(key)
            continue
        if is_placeholder(entry):
            classified["placeholder"].append(key)
            continue
        terms = subject_terms(entry)
        sites = []
        for t in terms:
            try:
                sites.extend(find_first_mentions(t, chapters))
            except re.error:
                continue
            if sites:
                break
        if sites:
            classified["orphan_should_cite"].append(key)
            cite_map[key] = [{"file": str(s[0]), "line": s[1], "snippet": s[2][:240]} for s in sites]
        else:
            classified["orphan_no_obvious_site"].append(key)

    DATA_FILE.write_text(json.dumps({
        "totals": {k: len(v) for k, v in classified.items()},
        "cited_total": len(cited),
        "bib_total": len(bib),
        "classified": classified,
        "cite_map": cite_map,
    }, indent=2), encoding="utf-8")

    # markdown report
    out = ["# Bibliography triage", ""]
    out.append(f"- bib total: **{len(bib)}**")
    out.append(f"- cited keys: **{len(cited)}**")
    out.append(f"- placeholder/fabricated: **{len(classified['placeholder'])}**")
    out.append(f"- orphan with likely cite-site: **{len(classified['orphan_should_cite'])}**")
    out.append(f"- orphan with no obvious cite-site: **{len(classified['orphan_no_obvious_site'])}**")
    out.append("")

    out.append("## Placeholder / fabricated entries (recommend DELETE)")
    for k in classified["placeholder"]:
        a = bib[k]["fields"].get("author", "?")
        t = bib[k]["fields"].get("title", "?")
        out.append(f"- `{k}` — {a} — _{t}_")
    out.append("")

    out.append("## Orphan entries with likely cite-site")
    out.append("")
    for k in classified["orphan_should_cite"]:
        title = bib[k]["fields"].get("title", "?")
        out.append(f"### `{k}` — _{title}_")
        for site in cite_map[k]:
            out.append(f"- {site['file']}:{site['line']} — `{site['snippet']}`")
        out.append("")

    out.append("## Orphan entries with no obvious cite-site (recommend REVIEW)")
    for k in classified["orphan_no_obvious_site"]:
        title = bib[k]["fields"].get("title", "?")
        out.append(f"- `{k}` — _{title}_")
    out.append("")

    OUT_FILE.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {OUT_FILE}")
    print(f"wrote {DATA_FILE}")
    for k, v in classified.items():
        print(f"  {k}: {len(v)}")


if __name__ == "__main__":
    main()
