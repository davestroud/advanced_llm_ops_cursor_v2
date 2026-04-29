#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="docs/audit_reports/citations_${TIMESTAMP}.md"
mkdir -p docs/audit_reports

{
  echo "# Citation Audit — $TIMESTAMP"
  echo ""

  # Catches \cite, \citep, \citet, \citeauthor, \citeyear, \citetitle, \citenum,
  # \parencite, \textcite, \autocite, \smartcite, \footcite, \fullcite.
  used_keys=$(grep -rhoE "\\\\(cite[a-z]*|parencite|textcite|autocite|smartcite|footcite|fullcite)\{[^}]+\}" ch*.tex 2>/dev/null \
              | sed -E 's/^\\(cite[a-z]*|parencite|textcite|autocite|smartcite|footcite|fullcite)\{//;s/\}$//' \
              | tr ',' '\n' | tr -d ' ' | sort -u)

  defined_keys=$(grep -E "^@" references.bib 2>/dev/null \
                 | sed -E 's/^@[a-zA-Z]+\{//;s/,.*$//' | sort -u)

  echo "## Dangling citations (cited in text but not in references.bib)"
  echo ""
  dangling=0
  for key in $used_keys; do
    if ! echo "$defined_keys" | grep -Fxq "$key"; then
      echo "- \`$key\`"
      dangling=$((dangling + 1))
    fi
  done
  [ "$dangling" = "0" ] && echo "PASS — none found"
  echo ""

  echo "## Orphan bib entries (in references.bib, never cited)"
  echo ""
  orphan=0
  for key in $defined_keys; do
    if ! echo "$used_keys" | grep -Fxq "$key"; then
      echo "- \`$key\`"
      orphan=$((orphan + 1))
    fi
  done
  [ "$orphan" = "0" ] && echo "PASS — none found"
  echo ""

  echo "## \\\\cite commands with spaces after commas"
  echo ""
  hits=$(grep -rnE "\\\\(cite[a-z]*|parencite|textcite|autocite|smartcite|footcite|fullcite)\{[^}]*, [^}]*\}" ch*.tex 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi
  echo ""

  echo "## Mixed citation styles (project uses numeric biblatex)"
  echo ""
  hits=$(grep -rnE "\\\\(citep|citet|citeauthor)\{" ch*.tex 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "PASS — none found"
  else
    echo "\`\`\`"
    echo "$hits"
    echo "\`\`\`"
  fi

  echo ""
  echo "**Totals:** $dangling dangling | $orphan orphan"

} > "$OUT"

echo "Report written to $OUT"
