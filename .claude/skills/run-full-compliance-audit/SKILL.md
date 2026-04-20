---
name: run-full-compliance-audit
description: Runs every Springer compliance audit in sequence and produces a single consolidated report with an executive summary. Use when the user asks to audit the entire book, run a full compliance check, prepare for Springer submission, or validate the manuscript before handoff.
---

# Full Compliance Audit

Runs all seven audit skills and consolidates output.

## Outputs

- `docs/audit_reports/FULL_AUDIT_<timestamp>.md` — full consolidated report
- `docs/audit_reports/LATEST_SUMMARY.md` — executive summary only (overwritten each run)

## Does NOT

- Modify any chapter file.
- Attempt to fix any issue.
- Invoke any LLM reasoning — orchestrates bash scripts only.

## Workflow

Run before every Overleaf sync, before every structure commit, and before
every submission to Springer. Run it again in Codex CLI to verify
deterministic output.
