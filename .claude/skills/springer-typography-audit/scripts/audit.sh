#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="docs/audit_reports/typography_${TIMESTAMP}.md"
mkdir -p docs/audit_reports

{
  echo "# Typography Audit — $TIMESTAMP"
  echo ""

  echo "## Forbidden font sizes (\\\\tiny, \\\\scriptsize)"
  echo ""
  hits=$(grep -rn "\\\\tiny\|\\\\scriptsize" ch*.tex 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi
  echo ""

  echo "## Raw \\\\paragraph or \\\\subparagraph (should be \\\\subsubsection)"
  echo ""
  hits=$(grep -rn "^\\\\paragraph{\|^\\\\subparagraph{" ch*.tex 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi
  echo ""

  echo "## Widths above 0.95\\\\linewidth"
  echo ""
  hits=$(grep -rnE "width=(0\.9[6-9]|1\.0|\\\\textwidth)" ch*.tex 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi
  echo ""

  echo "## Raster graphics in use (prefer vector)"
  echo ""
  hits=$(grep -rnE "includegraphics.*\.(png|jpg|jpeg)" ch*.tex 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi
  echo ""

  echo "## Manual vertical-spacing hacks (outside tables/TikZ/boxes)"
  echo ""
  hits=$(grep -rnE "\\\\(vspace|vfill|smallskip|medskip|bigskip)\{" ch*.tex 2>/dev/null \
         | grep -vE "tabular|TikZ|svgraybox|tcolorbox" || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits" | head -50
    echo "\`\`\`"
  fi
  echo ""

  echo "## Listing length and density"
  echo ""
  echo "| Chapter | codebox | minted | >80 lines | >150 lines | stray inline |"
  echo "|---------|--------:|-------:|----------:|-----------:|-------------:|"

  total_codebox=0
  total_minted=0
  total_warn=0
  total_fail=0
  total_stray=0
  chapters_overdense=""

  for f in ch*.tex; do
    [ -f "$f" ] || continue

    cb=$( (grep -c '\\begin{codebox}' "$f" 2>/dev/null || true) )
    cb=${cb:-0}
    mn=$( (grep -c '\\begin{minted}' "$f" 2>/dev/null || true) )
    mn=${mn:-0}

    counts=$(awk '
      BEGIN { in_codebox=0; in_minted=0; start=0; was_in_cb=0; warn=0; fail=0; stray=0 }
      /\\begin\{codebox\}/ { in_codebox=1 }
      /\\end\{codebox\}/   { in_codebox=0 }
      /\\begin\{minted\}/ {
        start = NR
        in_minted = 1
        was_in_cb = in_codebox
      }
      /\\end\{minted\}/ && in_minted {
        len = NR - start - 1
        if (was_in_cb == 0 && len <= 5) {
          stray++
        } else if (len > 150) {
          fail++
        } else if (len > 80) {
          warn++
        }
        in_minted = 0
      }
      END { print warn, fail, stray }
    ' "$f")
    warn=$(echo "$counts" | awk '{print $1}')
    fail=$(echo "$counts" | awk '{print $2}')
    stray=$(echo "$counts" | awk '{print $3}')

    total_codebox=$((total_codebox + cb))
    total_minted=$((total_minted + mn))
    total_warn=$((total_warn + warn))
    total_fail=$((total_fail + fail))
    total_stray=$((total_stray + stray))

    cb_label="$cb"
    if [ "$cb" -gt 8 ]; then
      cb_label="$cb (WARN >8)"
      chapters_overdense="$chapters_overdense $f"
    fi

    echo "| $f | $cb_label | $mn | $warn | $fail | $stray |"
  done

  echo ""
  echo "**Totals:** $total_codebox codebox / $total_minted minted | $total_warn WARN (>80 lines) | $total_fail FAIL (>150 lines) | $total_stray stray inline"
  echo ""
  echo "**Target range:** 40–45 codebox listings book-wide."
  if [ "$total_codebox" -gt 45 ]; then
    echo "- **Status:** over target ($total_codebox > 45). Reduction work indicated."
  elif [ "$total_codebox" -lt 40 ]; then
    echo "- **Status:** under target ($total_codebox < 40). Possibly over-compressed."
  else
    echo "- **Status:** within target ($total_codebox in 40–45)."
  fi
  if [ -n "$chapters_overdense" ]; then
    echo "- **Over-dense chapters (>8 listings):**$chapters_overdense"
  fi

} > "$OUT"

echo "Report written to $OUT"
