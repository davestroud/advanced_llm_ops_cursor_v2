# CLAUDE.md — Agent Orientation

This file is read first by any Claude or Codex agent working in this repo.
It orients the agent, points to authoritative rules, and lists the skills
available for common tasks. It is navigation, not a rulebook.

## What this repo is

*Advanced Large Language Model Operations — Best Practices and Key Concepts*
by David Stroud. Springer Nature monograph using the `SNmono` document
class (pdfLaTeX + biber). 12 chapters, 4 parts, ~21,000 lines of LaTeX,
~450 bibliography entries. Running case study: Ishtar AI — a conflict-zone
journalism assistant.

## Where rules live (authoritative sources, in order)

1. `.cursor/rules/book-rules.mdc` — always-applied Cursor rules. Primary
   style and structure contract. Read in full before any structural change.
2. `paper_spec.md` — project charter. Short.
3. `docs/SPRINGER_COMPLIANCE_REPORT.md` — per-chapter audit history.
   Read before repeating prior work.
4. Springer Nature Manuscript Guidelines (external) — ultimate authority.
   Cited inline in each skill where relevant.
5. This file — navigation only.

If a rule conflicts across sources, Springer's guidelines win, then
`book-rules.mdc`, then this file. Flag conflicts to the author; do not
silently resolve.

## Build

```
latexmk -pdf book.tex           # full build
latexmk -C                      # clean aux files
grep -c "Warning" book.log      # warning count (track against baseline)
```

If you add a package requiring shell-escape (e.g. `minted`), update
`latexmkrc.tex` and document the dependency in
`docs/SPRINGER_COMPLIANCE_REPORT.md`.

## Critical project conventions (summary — full rules in book-rules.mdc)

- **Labels:** `fig:chXX_slug`, `tab:chXX_slug`, `alg:chXX_slug`,
  `lst:chXX_slug`, `eq:chXX_slug`, `ch:<short-id>`.
- **Cross-references in prose:** `Figure~\ref{...}`, `Table~\ref{...}`,
  `Listing~\ref{...}`, `Algorithm~\ref{...}`, `Equation~\ref{...}`,
  `Section~\ref{...}` — always with the non-breaking tie, always spelled
  out (no "Fig." or "Tab.").
- **Float placement:** `[t]` by default, `[tb]` if needed. No `[H]` or
  `[h!]` without justification in adjacent prose.
- **Widths:** max `0.95\linewidth`.
- **Fonts in graphics:** minimum `\footnotesize`, prefer `\small`, never
  `\tiny` or `\scriptsize`.
- **Grayscale safety:** charts must remain distinguishable in B&W; use
  dash patterns AND marker shapes, not color alone.
- **Captions:** lead with the reader takeaway (what the reader learns),
  not a description of contents.
- **Sectioning depth:** `\section` → `\subsection` → `\subsubsection`.
  No `\paragraph` or `\subparagraph`.
- **Case study:** always use the `\ishtar` macro (renders "Ishtar AI").
  Never hand-type.

## Ishtar AI — voice

Mission-critical tone. Stakes are real: lives, source safety, journalistic
accuracy. Avoid cuteness. Use `\ishtar`, never "Ishtar" or "Ishtar.ai"
in raw text.

## Skills available

Skills live in `.claude/skills/<skill-name>/SKILL.md` and are auto-loaded
when their descriptions match the task. All skills in this repo are
audit-only — they produce reports, never mutate files.

| Skill                           | Purpose                                              |
|---------------------------------|------------------------------------------------------|
| `springer-structure-audit`      | Parts, chapters, abstracts, front/back matter        |
| `springer-float-audit`          | Figures, tables, listings: placement, labels, refs   |
| `springer-typography-audit`     | Fonts, widths, grayscale safety, sectioning depth    |
| `springer-citation-audit`       | Orphan refs, uncited bib entries, cite-format issues |
| `springer-cross-ref-audit`      | Every label referenced, every ref has a target       |
| `springer-accessibility-audit`  | Caption takeaways, alt-text hints, index density     |
| `springer-ai-declaration-audit` | Springer's LLM/generative-AI policy compliance       |
| `run-full-compliance-audit`     | Runs all of the above; produces consolidated report  |

Auto-invoked by natural-language requests. Force a specific skill with
`/<skill-name>`.

## What NOT to do

- Do not modify citations, labels, or author prose during an audit.
- Do not duplicate `book-rules.mdc` content into this file or skills.
- Do not invent Springer requirements not in the published guidelines.
- Do not skip build validation after changes. Warning count stays ≤ baseline.

## Cross-tool compatibility (Claude Code ↔ Codex CLI)

Agent Skills is an open standard (December 2025). The `SKILL.md` files in
`.claude/skills/` work identically in Claude Code and Codex CLI. The author
uses Codex to verify Claude's work. Therefore every skill must be
deterministic and produce machine-checkable output.
