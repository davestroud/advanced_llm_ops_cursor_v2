#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="docs/audit_reports/floats_${TIMESTAMP}.md"
mkdir -p docs/audit_reports

{
  echo "# Float Audit — $TIMESTAMP"
  echo ""
  echo "## Per-chapter summary"
  echo ""
  echo "| Chapter | Figures | Tables | Listings | Bad floats | Weak captions |"
  echo "|---------|---------|--------|----------|------------|---------------|"

  total_bad=0
  total_weak=0

  for f in ch*.tex; do
    [ -f "$f" ] || continue
    figs=$(grep -c "^\\\\begin{figure}" "$f" 2>/dev/null || true); figs=${figs:-0}
    tabs=$(grep -c "^\\\\begin{table}" "$f" 2>/dev/null || true); tabs=${tabs:-0}
    lsts=$(grep -cE "^\\\\begin\{(lstlisting|codebox)\}" "$f" 2>/dev/null || true); lsts=${lsts:-0}
    bad=$(grep -cE "\\\\begin\{(figure|table)\}\[(H|h!|h)\]" "$f" 2>/dev/null || true); bad=${bad:-0}
    weak=$(grep -cE "caption\{(A diagram showing|This figure depicts|Illustration of|Example of|Shows |Figure showing)" "$f" 2>/dev/null || true); weak=${weak:-0}
    echo "| $f | $figs | $tabs | $lsts | $bad | $weak |"
    total_bad=$((total_bad + bad))
    total_weak=$((total_weak + weak))
  done

  echo ""
  echo "**Totals:** $total_bad bad-float specifiers | $total_weak weak caption openings"
  echo ""

  echo "## Orphan artifact labels (defined but never \\\\ref'd)"
  echo ""
  for label in $({ grep -rhoE "label\{(fig|tab|lst|alg):ch[0-9]+_[a-zA-Z0-9_]+\}" ch*.tex 2>/dev/null || true; } \
                 | sed 's/label{//;s/}$//' | sort -u); do
    refs=$({ grep -rEc "ref\{$label\}" ch*.tex 2>/dev/null || true; } | awk -F: '{s+=$2} END {print s+0}')
    if [ "$refs" -eq 0 ]; then
      echo "- \`$label\`"
    fi
  done
  echo ""

  echo "## Dangling references (\\\\ref with no \\\\label)"
  echo ""
  for ref in $({ grep -rhoE "ref\{(fig|tab|lst|alg|eq|ch|sec):[a-zA-Z0-9_:-]+\}" ch*.tex 2>/dev/null || true; } \
               | sed 's/ref{//;s/}$//' | sort -u); do
    defs=$({ grep -rEc "label\{$ref\}" ch*.tex 2>/dev/null || true; } | awk -F: '{s+=$2} END {print s+0}')
    if [ "$defs" -eq 0 ]; then
      echo "- \`$ref\`"
    fi
  done

} > "$OUT"

echo "Report written to $OUT"
