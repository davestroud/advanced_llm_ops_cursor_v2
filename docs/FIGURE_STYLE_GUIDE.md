# Figure Style Guide

Single source of truth for all figures in *Advanced LLMOps* (Springer textblock).
Every figure in the book **must** comply with the rules below. The macros that
implement these rules live at the end of `macros.tex`.

---

## 1. Vector-only policy

All figures must be vector art. Raster images (`.png`, `.jpg`) are **not**
permitted in the main text. Existing raster figures must be converted to one of:

- `tikzpicture` for conceptual diagrams, architectures, flows.
- `axis` (PGFPlots) for data-driven charts.
- A PDF exported from a vector source (Draw.io SVG -> PDF, Inkscape -> PDF)
  only when TikZ authoring is impractical. In that case the PDF must be
  embedded via `\includegraphics[width=0.95\linewidth]{...}`.

Rationale: Springer prints at up to 600 dpi and rasters at book textblock width
(5.5 in / 14 cm) visibly pixelate. Vector art also re-scales cleanly into the
ebook and PDF outputs.

## 2. Float placement and width

Every figure uses:

```latex
\begin{figure}[t]              % top of page, never [h] or [H]
  \centering
  \begin{llmfigbox}            % wrapper defined in macros.tex
    ... tikzpicture / axis / includegraphics ...
  \end{llmfigbox}
  \caption{Reader takeaway sentence. Supporting detail.}
  \label{fig:chXX_<slug>}
\end{figure}
```

- `\begin{figure}[t]` only. Do not use `[h]`, `[H]`, `[!h]`, or `[p]`.
- Width is capped at `0.95\linewidth`. Never exceed this. Use less if the
  intrinsic aspect ratio of the figure is short and wide.
- Use `llmfigbox` (see `macros.tex`). It enforces max-width, centring, and
  consistent top/bottom spacing.

## 3. Caption discipline

Every caption follows the two-sentence Springer takeaway pattern:

1. **First sentence** states what the reader should *take away* from the
   figure. It must be a full sentence ending in a period.
2. **Second sentence** (optional) provides supporting detail, parameter
   values, data source, or interpretation hints.

Bad: `\caption{System architecture.}`
Good: `\caption{The retrieval pipeline hides vector-store latency behind a caching layer so end-to-end p95 stays under 400ms. Numbers reflect ch.~6 load test at 50 QPS.}`

## 4. Label namespace

All figure labels follow:

```
fig:chXX_<slug>
```

where `XX` is zero-padded chapter number (`ch01`...`ch12`) and `<slug>` is a
short lowercase snake_case description. Labels are immutable once referenced.

## 5. Cross-reference requirement

Every figure must be cross-referenced at least once in the surrounding prose
via `\Cref{fig:chXX_<slug>}` (preferred) or `Figure~\ref{...}`. Figures that
appear without a textual reference are flagged in the audit.

## 6. Grayscale safety

The book prints in monochrome. Diagrams must therefore:

- Use the book palette (`llmblue`, `llmorange`, `llmgreen`, `llmpurple`,
  `llmgray`), which is lightness-separated by >=12 L* between adjacent slots.
- Distinguish multiple series by **both** color and shape/dash pattern. The
  `llm/cycle` PGFPlots cycle list already enforces this.
- Never rely on hue alone to encode meaning (e.g. "the red line is bad") -
  always label or annotate.

## 7. Typography

- Minimum font size inside a figure: `\footnotesize`. Never smaller than
  `\scriptsize`, and only for legends or axis ticks when space is tight.
- All labels use the document font (no `\sffamily` overrides, no Computer
  Modern italic for proper nouns).
- Node text is centred inside shapes; prose labels outside nodes use
  `llm/label` style.

## 8. Line weights

- Diagram borders: `0.6pt` (set by `llm/box`).
- Arrows: `0.7pt` (set by `llm/arrow`).
- Plot lines: `1.2pt` (set by `llm/chart`'s `every axis plot/.append style`).
- Grid: `0.3pt`, 15% black (set by `llm/chart`).

Thinner than `0.3pt` disappears at print DPI; thicker than `1.5pt` looks
cartoonish.

## 9. Style macros - mandatory use

**Boxes / nodes** - use `llm/box` as the base style, then one of the five
color variants:

```latex
\node[llm/box/blue]   (a) {Component};
\node[llm/box/orange] (b) {Component};
```

**Arrows** - use `llm/arrow` (solid) or `llm/arrow/dashed` (dependency,
feedback, async):

```latex
\draw[llm/arrow] (a) -- (b);
\draw[llm/arrow/dashed] (b) -- (a);
```

**Lane / group** - use `llm/lane` for swimlane containers; `llm/label` for
free-floating text annotations.

**Charts** - every `\begin{axis}[...]` must apply both `llm/chart` and
`llm/cycle`:

```latex
\begin{axis}[llm/chart, llm/cycle, xlabel={...}, ylabel={...}]
  \addplot table {data1};
  \addplot table {data2};
\end{axis}
```

Hardcoded colors, font sizes, or line widths inside a `tikzpicture` are a
style violation and flagged by the audit.

## 10. Accessibility

- Alt-text equivalent must appear in the caption's first sentence.
- Do not encode meaning in position alone; always label nodes.
- Avoid 3-D effects, drop shadows, and gradient fills. The book palette has
  flat fills only.

## 11. Compile contract

- Figures must compile with `pdflatex -shell-escape` using TeX Live 2023+.
- `pgfplots` `compat=1.18` or later.
- No dependency on Asymptote, Metapost, or external SVG converters during
  the main build.

## 12. Enforcement

The audit at `docs/FIGURE_AUDIT.md` records every violation of the rules
above. A figure is considered compliant only when it passes all twelve
sections of this guide.
