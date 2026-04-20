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

} > "$OUT"

echo "Report written to $OUT"
