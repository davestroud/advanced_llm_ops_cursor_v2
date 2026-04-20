# Book Compliance Skills

All skills in this directory follow these conventions:

1. **Audit-only by default.** Skills produce a report in
   `docs/audit_reports/<name>_<timestamp>.md`. They never mutate `.tex` files.
2. **Deterministic.** Same input → same output. No LLM inference in the
   audit body; only extracted facts and rule references.
3. **Machine-checkable output.** Markdown tables or JSON. Codex must be
   able to reproduce identical output.
4. **Cite your source.** Every rule check links to either
   `.cursor/rules/book-rules.mdc` (with line context) or a Springer
   Manuscript Guidelines section.
5. **Idempotent.** Running twice produces the same report (modulo timestamp).
6. **Fail open.** Unknown constructs flagged MANUAL, never silently passed.

Directory structure per skill:

    .claude/skills/<skill-name>/
    ├── SKILL.md              (required: YAML frontmatter + instructions)
    └── scripts/
        └── audit.sh          (required: bash, deterministic, no LLM calls)

Status legend used in reports:
- `PASS`    — check succeeded
- `FAIL`    — check failed; action required before submission
- `WARN`    — check raised a concern; review recommended
- `MANUAL`  — check produced signals a human must interpret
