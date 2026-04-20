#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="docs/audit_reports/cross_refs_${TIMESTAMP}.md"
mkdir -p docs/audit_reports

{
  echo "# Cross-Reference Audit — $TIMESTAMP"
  echo ""

  all_labels=$(grep -rhoE "label\{[a-zA-Z0-9_:-]+\}" ch*.tex 2>/dev/null \
               | sed 's/label{//;s/}$//' | sort -u)
  all_refs=$(grep -rhoE "ref\{[a-zA-Z0-9_:-]+\}" ch*.tex 2>/dev/null \
             | sed 's/ref{//;s/}$//' | sort -u)

  echo "## Labels never referenced (potentially orphan artifacts)"
  echo ""
  orphan=0
  for L in $all_labels; do
    if ! echo "$all_refs" | grep -Fxq "$L"; then
      echo "- \`$L\`"
      orphan=$((orphan + 1))
    fi
  done
  [ "$orphan" = "0" ] && echo "PASS — none found"
  echo ""

  echo "## \\\\ref targets with no \\\\label (broken references)"
  echo ""
  broken=0
  for R in $all_refs; do
    if ! echo "$all_labels" | grep -Fxq "$R"; then
      echo "- \`$R\`"
      broken=$((broken + 1))
    fi
  done
  [ "$broken" = "0" ] && echo "PASS — none found"
  echo ""

  echo "## 'Above/below' where an explicit reference may be better"
  echo ""
  hits=$(grep -rnE "(figure|table|listing|algorithm|equation) (above|below)" ch*.tex 2>/dev/null | head -50 || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi

  echo ""
  echo "**Totals:** $orphan orphan labels | $broken broken references"

} > "$OUT"

echo "Report written to $OUT"
