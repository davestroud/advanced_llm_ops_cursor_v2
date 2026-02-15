# Paper Specification: Advanced Large Language Model Operations

## Document Type
Springer Nature Monograph (svmono class)

## Author
David Stroud

## Structure
- 4 Parts, 12 Chapters
- Front matter: dedication, foreword, preface, acknowledgements, TOC, acronyms, notation
- Back matter: glossary, index
- Per-chapter bibliographies (biblatex + biber, refsegment=chapter)

## Springer Formatting Requirements
- Float placement: [t] default, [tb] if needed, avoid [H]
- Label prefixes: fig:chXX_, tab:chXX_, alg:chXX_, lst:chXX_
- Captions must state reader takeaway
- All artifacts referenced in prose within +/-1 paragraph
- Max width: 0.95\linewidth
- Min font size: \footnotesize (prefer \small)
- Vector graphics preferred (TikZ/PGFPlots)
- Grayscale-safe (no color-only meaning)
- Use svgraybox for callout boxes (BestPractice, Pitfall, Definition, Checklist, IshtarVignette)

## Case Study
Ishtar AI - A conflict-zone journalism AI assistant using RAG, multi-agent orchestration, and GPU-backed serving. Referenced in every chapter via \ishtar macro.

## Custom Macros (defined in macros.tex)
- \BestPracticeBox{}, \PitfallBox{}, \DefinitionBox{}, \ChecklistBox{}, \IshtarVignette{}
- llmfigbox, llmfigboxnoscale environments
- \ishtar command

## Known Issues to Fix
- ~69 unreferenced figures/tables need in-text \ref{} citations
- Caption quality improvements needed (takeaway language)
- Ch08 float placement issues
- Ch11 (Ethics) notably shorter than other chapters
- Empty front/back matter: dedication, foreword, preface, acknowledgements, glossary, acronyms, appendix
