#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="docs/audit_reports/ai_declaration_${TIMESTAMP}.md"
mkdir -p docs/audit_reports

{
  echo "# AI-Use Declaration Audit — $TIMESTAMP"
  echo ""
  echo "Springer requires LLM use to be declared in acknowledgements."
  echo "Springer does not accept generative-AI figures (narrow exceptions)."
  echo ""

  echo "## Acknowledgements declaration"
  echo ""
  ack="author/acknowledgement.tex"
  if [ -f "$ack" ]; then
    if grep -qiE "LLM|large language model|generative AI|Claude|GPT|artificial intelligence|AI assistant" "$ack"; then
      echo "- Declaration present — **MANUAL REVIEW**: confirm wording matches Springer policy"
    else
      echo "- **NO DECLARATION** found — FAIL if any AI assistance was used in drafting"
    fi
  else
    echo "- Acknowledgement file missing — FAIL"
  fi
  echo ""

  echo "## Raster figures in chapter source"
  echo ""
  hits=$(grep -rnE "includegraphics.*\.(png|jpg|jpeg)" ch*.tex 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "PASS — no raster includes found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi
  echo ""

  echo "## Files in images/ directory"
  echo ""
  if [ -d images ]; then
    (cd images && ls -1 | sort) | while read img; do echo "- \`$img\`"; done
  else
    echo "- No images/ directory"
  fi

} > "$OUT"

echo "Report written to $OUT"
