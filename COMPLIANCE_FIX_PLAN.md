# Compliance Fix Plan - Per Chapter

## Critical Violations Found

### Width Violations (Must Fix)
- **ch01-intro-ishar.tex**: 2 instances of `width=0.98\textwidth` (should be ≤ 0.95\linewidth)
- **ch12-ishtar-end-to-end.tex**: 2 instances of `width=0.96\textwidth` (should be ≤ 0.95\linewidth)

### Missing TikZ Wrappers (Must Fix)
- **ch06-scaling.tex**: 8 TikZ figures but only 6 wrapped with llmfigbox (2 missing)

### Unreferenced Artifacts (Should Fix)
- **ch01**: 11 unreferenced
- **ch02**: 5 unreferenced
- **ch03**: 9 unreferenced
- **ch04**: 5 unreferenced
- **ch05**: 5 unreferenced
- **ch06**: 11 unreferenced
- **ch07**: 15 unreferenced
- **ch08**: 4 unreferenced
- **ch09**: 1 unreferenced
- **ch12**: 3 unreferenced

## Fix Priority

### Priority 1: Critical (Must Fix)
1. Width violations (ch01, ch12)
2. Missing llmfigbox wrappers (ch06)

### Priority 2: Important (Should Fix)
3. Add references for key artifacts (all chapters)

### Priority 3: Nice-to-Have (Can Fix Later)
4. Caption quality improvements
5. Callout box standardization

## Fix Strategy

### Step 1: Fix Width Violations
- Change `width=0.98\textwidth` → `width=0.95\linewidth`
- Change `width=0.96\textwidth` → `width=0.95\linewidth`

### Step 2: Fix Missing TikZ Wrappers
- Find unwrapped TikZ figures in ch06
- Add llmfigbox wrappers

### Step 3: Add Artifact References
- For each unreferenced artifact, add reference in prose within ±1 paragraph
- Use proper format: `Fig.~\ref{...}` or `Table~\ref{...}`

