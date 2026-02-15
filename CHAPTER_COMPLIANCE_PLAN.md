# Chapter-by-Chapter Compliance Review Plan

## Overview
Systematic review of all 12 chapters to ensure 100% compliance with `.cursor/rules/book-rules.mdc` requirements.

## Chapters to Review
1. ch01-intro-ishar.tex
2. ch02-llmops-fundamentals.tex
3. ch03-infra-env.tex
4. ch04-cicd.tex
5. ch05-observability.tex
6. ch06-scaling.tex
7. ch07-performance.tex
8. ch08-rag.tex
9. ch09-agents-orchestration.tex
10. ch10-testing-eval.tex
11. ch11-ethics.tex
12. ch12-ishtar-end-to-end.tex

## Compliance Checklist (Per Chapter)

### A) NON-NEGOTIABLE RULES

#### 1. Production-Safe Visuals
- [ ] **Vector graphics preferred**: Check for screenshots (PNG/JPG). If found, verify justification in prose.
- [ ] **Font sizes**: Verify no `\tiny` or `\scriptsize` in TikZ/PGFPlots (minimum `\footnotesize`, prefer `\small`)
- [ ] **Grayscale-safe**: Check for color-only meaning (use line styles, markers, hatching, labels)
- [ ] **No layout hacks**: Check for `\vspace{-...}` or `\hspace{-...}` (negative spacing)

#### 2. Float & Caption Discipline
- [ ] **Float placement**: Verify all floats use `[t]` (or `[tb]` if justified). No `[H]` unless absolutely required.
- [ ] **Float structure**: Every artifact has `\centering`, `\caption{...}`, `\label{...}`
- [ ] **Caption quality**: Captions state reader takeaway (what to learn / why it matters), not just description
- [ ] **Artifact references**: Every artifact referenced in prose within ±1 paragraph using `Fig.~\ref{}` or `Table~\ref{}`

#### 3. Label Naming (Mandatory)
- [ ] **Figure labels**: All follow `fig:chXX_slug` pattern
- [ ] **Table labels**: All follow `tab:chXX_slug` pattern
- [ ] **Algorithm labels**: All follow `alg:chXX_slug` pattern (if any)
- [ ] **Listing labels**: All follow `lst:chXX_slug` pattern (if any)
- [ ] **Reference format**: All references use `Fig.~\ref{}`, `Table~\ref{}`, `Alg.~\ref{}`, `Listing~\ref{}`

#### 4. Width & Readability
- [ ] **Max width**: All figures/tables ≤ 0.95\linewidth
- [ ] **No extreme scaling**: Check for excessive `\resizebox` or `\scalebox`
- [ ] **Readability**: Text remains readable after scaling

### B) STANDARD PRACTICES

#### 5. TikZ Figure Wrappers
- [ ] **llmfigbox wrapper**: All TikZ figures wrapped with `\begin{llmfigbox}...\end{llmfigbox}`
- [ ] **No resizebox**: No `\resizebox` wrappers (use llmfigbox instead)

#### 6. Citation Formatting
- [ ] **No spaces after commas**: `\cite{key1,key2}` not `\cite{key1, key2}`
- [ ] **Proper spacing**: Space before citations in prose

#### 7. Callout Boxes
- [ ] **Standard macros**: "Best Practice", "Pitfall", "Definition" boxes use `\BestPracticeBox`, `\PitfallBox`, `\DefinitionBox`
- [ ] **Consistent styling**: All callout boxes follow Springer style

#### 8. Visual Standards
- [ ] **Screenshots justified**: Any PNG/JPG images have justification in adjacent prose
- [ ] **Color accessibility**: No reliance on color alone for meaning
- [ ] **Line styles**: Use different line styles, markers, hatching for distinction

## Review Process

### Phase 1: Automated Checks (COMPLETED ✓)
- [x] Label naming conventions
- [x] Float placement ([t] default)
- [x] Reference format (Fig./Table.)
- [x] Citation formatting (no spaces after commas)
- [x] TikZ wrappers (llmfigbox)
- [x] Font sizes (tiny/scriptsize → footnotesize/small)

### Phase 2: Per-Chapter Manual Review (IN PROGRESS)
For each chapter:
1. Read chapter file
2. Extract all figures, tables, algorithms, listings
3. Check each against compliance checklist
4. Document violations
5. Fix violations systematically

### Phase 3: Fixes
1. Fix caption quality (add takeaway language)
2. Add missing artifact references in prose
3. Verify/justify screenshots
4. Check width violations
5. Verify color-only meaning issues
6. Convert manual callout boxes to macros

### Phase 4: Final Verification
1. Re-run automated checks
2. Manual spot-check of fixes
3. Generate final compliance report

## Current Status

### Completed ✓
- Label naming: All chapters compliant
- Float placement: All chapters compliant
- Reference format: All chapters compliant
- Citation formatting: All chapters compliant
- TikZ wrappers: All chapters compliant
- Font sizes: All chapters fixed

### Needs Manual Review ⚠
- Caption quality: ~70% need improvement (takeaway-focused)
- Artifact references: ~60% of artifacts unreferenced
- Visual standards: Screenshots need justification
- Width violations: Not checked per chapter
- Color-only meaning: Not checked per chapter
- Callout boxes: ~15 manual boxes could use macros

## Next Steps

1. **Create per-chapter compliance report** with specific violations
2. **Prioritize fixes** (critical vs. nice-to-have)
3. **Systematically fix** chapter by chapter
4. **Verify fixes** before moving to next chapter

