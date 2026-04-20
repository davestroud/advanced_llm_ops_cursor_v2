#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="docs/audit_reports/accessibility_${TIMESTAMP}.md"
mkdir -p docs/audit_reports

{
  echo "# Accessibility Audit — $TIMESTAMP"
  echo ""

  echo "## Captions starting with passive-contents language"
  echo ""
  hits=$(grep -rnE "caption\{(A diagram showing|This figure depicts|Illustration of|Example of|Shows |Figure showing)" ch*.tex 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi
  echo ""

  echo "## Suspiciously short captions (< 20 chars)"
  echo ""
  hits=$(grep -rnE "caption\{[^}]{1,19}\}" ch*.tex 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi
  echo ""

  echo "## Empty captions"
  echo ""
  hits=$(grep -rnE "caption\{\}" ch*.tex 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi
  echo ""

  echo "## Index entries per chapter (target ≥ 10)"
  echo ""
  for f in ch*.tex; do
    [ -f "$f" ] || continue
    n=$(grep -c "\\\\index{" "$f" 2>/dev/null || true); n=${n:-0}
    if [ "$n" -lt 10 ]; then
      echo "- $f: $n entries — WARN"
    else
      echo "- $f: $n entries — OK"
    fi
  done

} > "$OUT"

echo "Report written to $OUT"
