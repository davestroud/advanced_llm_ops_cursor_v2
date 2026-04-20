#!/usr/bin/env bash
# audit_figures.sh
#
# Read-only audit of every \begin{figure}...\end{figure} float in the book.
# Produces two flat text files in docs/:
#
#   FIGURE_AUDIT_RAW.txt
#       One line per figure. Pipe-separated columns:
#       chapter | file | figure_start_line | label | type | float | wrapped | width | caption_first_sentence | caption_line
#
#       type    : tikz | pgfplots | includegraphics | other
#       float   : [t], [h], [H], etc. ("none" if absent)
#       wrapped : llmfigbox | none
#       width   : from \includegraphics / \begin{tikzpicture}/axis hints
#
#   FIGURE_REFS.txt
#       One line per unique figure label. Columns:
#       label | ref_count
#
# Usage (from repo root):
#   bash scripts/audit_figures.sh
#
# Exits 0 on success. Does not modify any .tex file.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

OUT_RAW="docs/FIGURE_AUDIT_RAW.txt"
OUT_REFS="docs/FIGURE_REFS.txt"
mkdir -p docs

CHAPTERS=(ch01-intro-ishar.tex ch02-llmops-fundamentals.tex ch03-infra-env.tex \
          ch04-cicd.tex ch05-observability.tex ch06-scaling.tex \
          ch07-performance.tex ch08-rag.tex ch09-agents-orchestration.tex \
          ch10-testing-eval.tex ch11-ethics.tex ch12-ishtar-end-to-end.tex)

: > "$OUT_RAW"

for f in "${CHAPTERS[@]}"; do
  [[ -f "$f" ]] || { echo "missing: $f" >&2; continue; }
  chap=$(printf '%s' "$f" | sed -nE 's/^ch([0-9]+).*$/\1/p')

  awk -v file="$f" -v chap="$chap" '
    BEGIN{
      depth=0; fig_start=0;
      label=""; type=""; float=""; wrapped=""; width=""; cap=""; cap_line=0;
    }
    function flush(   p){
      if (label == "") label = "NO_LABEL";
      if (type  == "") type  = "other";
      if (float == "") float = "none";
      if (wrapped == "") wrapped = "none";
      if (width == "") width = "n/a";
      gsub(/\|/, "/", cap);
      printf("%s|%s|%d|%s|%s|%s|%s|%s|%s|%d\n",
             chap, file, fig_start, label, type, float, wrapped, width, cap, cap_line);
    }
    {
      line = $0;
      # Strip comments (simple heuristic; does not handle escaped %)
      sub(/(^|[^\\])%.*$/, "", line);

      if (line ~ /\\begin\{figure\}/) {
        depth = 1; fig_start = NR;
        label=""; type=""; float=""; wrapped=""; width=""; cap=""; cap_line=0;
        if (match(line, /\\begin\{figure\}\[[^]]*\]/)) {
          tok = substr(line, RSTART, RLENGTH);
          m = match(tok, /\[[^]]*\]/);
          float = substr(tok, RSTART, RLENGTH);
        } else {
          float = "none";
        }
        next;
      }
      if (depth > 0) {
        if (line ~ /\\end\{figure\}/) { flush(); depth=0; next; }

        if (line ~ /\\begin\{llmfigbox\}/) wrapped = "llmfigbox";
        if (line ~ /\\begin\{tikzpicture\}/ && type == "") type = "tikz";
        if (line ~ /\\begin\{axis\}/ || line ~ /\\begin\{semilogyaxis\}/ || \
            line ~ /\\begin\{loglogaxis\}/ || line ~ /\\begin\{polaraxis\}/) type = "pgfplots";
        if (line ~ /\\includegraphics/ && type == "") type = "includegraphics";

        # Width hints
        if (match(line, /width=[^,\]}]*/)) {
          if (width == "n/a" || width == "") width = substr(line, RSTART+6, RLENGTH-6);
          else width = width ";" substr(line, RSTART+6, RLENGTH-6);
        }

        # Label
        if (match(line, /\\label\{[^}]+\}/)) {
          tok = substr(line, RSTART+7, RLENGTH-8);
          if (label == "") label = tok;
        }

        # Caption: grab first sentence of first \caption{...} found.
        if (cap == "" && match(line, /\\caption\{/)) {
          cap_line = NR;
          rest = substr(line, RSTART+9);
          # accumulate until matching close brace or EOL
          buf = rest;
          open = 1;
          for (i=1; i<=length(buf); i++) {
            c = substr(buf, i, 1);
            if (c == "{") open++;
            else if (c == "}") { open--; if (open == 0) { buf = substr(buf,1,i-1); break; } }
          }
          cap = buf;
          # First sentence: text before first period+space or end.
          if (match(cap, /\.[ ]/)) {
            cap = substr(cap, 1, RSTART);
          }
          gsub(/^[ \t]+|[ \t]+$/, "", cap);
        }
      }
    }
  ' "$f" >> "$OUT_RAW"
done

# ---- FIGURE_REFS.txt ------------------------------------------------------
: > "$OUT_REFS"

labels=$(awk -F'|' '$4 != "NO_LABEL" {print $4}' "$OUT_RAW" | sort -u)
for lbl in $labels; do
  # Count \ref{lbl}, \Cref{lbl}, \cref{lbl}, \pageref{lbl}, \autoref{lbl}
  # across all chapter files, excluding the defining \label itself.
  n=$(grep -E "\\\\(ref|Cref|cref|pageref|autoref)\{$lbl\}" ch*.tex 2>/dev/null | wc -l | tr -d ' ' || true)
  n=${n:-0}
  printf '%s|%s\n' "$lbl" "$n" >> "$OUT_REFS"
done

echo "Wrote:"
echo "  $OUT_RAW   ($(wc -l < "$OUT_RAW" | tr -d ' ') figures)"
echo "  $OUT_REFS  ($(wc -l < "$OUT_REFS" | tr -d ' ') labels)"
