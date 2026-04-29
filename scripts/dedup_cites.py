#!/usr/bin/env python3
"""Consolidate duplicate bib keys: rewrite cite commands to use a canonical key.

Maps each old (duplicate) key to its canonical replacement. Logs every change.
Does NOT delete bib entries (use bib_delete_keys.py for that).
"""
from __future__ import annotations
import re
import sys
import json
from pathlib import Path

CITE_RE = re.compile(
    r'\\(cite[a-z]*|parencite|textcite|autocite|smartcite|footcite|fullcite)\{([^}]+)\}',
)

# canonical -> [old_keys]
DEDUP = {
    'lambda': ['lambda-gpt3-cost'],
    'langsmith': ['langsmith_eval', 'langsmithDocs1', 'langsmithDocs2', 'langsmith_eval_docs'],
    'Chen2023SpeculativeSampling': ['leviathan2023speculative'],
    'nvidia_mig_guide': ['nvidia-mig-user-guide'],
    'openai_evals': ['openaievals'],
    'OWASP2024LLMTop10': ['owasp_llm_top10'],
    'promptfoo': ['promptfoo1', 'promptfoo2'],
    'tensorrt_llm_docs': ['tensorrtllm_docs'],
    'zheng2023judge': ['zheng2023mtbench'],
    'Kwon2023vLLM': ['vllm2023', 'pagedattention_vllm'],
    'helm': ['helm2022'],
    'fabricatedknowledge': ['fabricated-knowledge-costs'],
}

# Build flat old->new map
old_to_new = {}
for canonical, olds in DEDUP.items():
    for o in olds:
        old_to_new[o] = canonical


def process_file(path: Path) -> tuple[int, list[dict]]:
    text = path.read_text()
    actions: list[dict] = []
    new_text = text

    def repl(m):
        cmd = m.group(1)
        keys = [k.strip() for k in m.group(2).split(',')]
        new_keys = [old_to_new.get(k, k) for k in keys]
        # de-dup while preserving order
        seen = set(); dedup = []
        for k in new_keys:
            if k not in seen:
                seen.add(k); dedup.append(k)
        if dedup != keys:
            actions.append({
                'file': str(path), 'cmd': cmd,
                'before': keys, 'after': dedup,
            })
            return f'\\{cmd}{{{",".join(dedup)}}}'
        return m.group(0)

    new_text = CITE_RE.sub(repl, text)
    if new_text != text:
        path.write_text(new_text)
    return len(actions), actions


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: dedup_cites.py <log_path> <file1> [file2 ...]")
        return 2
    log_path = Path(sys.argv[1])
    total = 0
    all_actions: list[dict] = []
    for fp in sys.argv[2:]:
        path = Path(fp)
        if not path.exists():
            continue
        n, acts = process_file(path)
        if n:
            print(f"  {fp}: {n} cite commands updated")
        total += n
        all_actions.extend(acts)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(all_actions, indent=2))
    print(f"Total: {total} cite commands updated. Log -> {log_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
