#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="docs/audit_reports/structure_${TIMESTAMP}.md"
mkdir -p docs/audit_reports

{
  echo "# Springer Structure Audit — $TIMESTAMP"
  echo ""
  echo "| Check | Status | Location | Reference |"
  echo "|-------|--------|----------|-----------|"

  # 1. Part count
  part_count=$(grep -c "^\\\\part{" book.tex 2>/dev/null || true)
  part_count=${part_count:-0}
  if [ "$part_count" = "4" ]; then
    echo "| Part count = 4 | PASS | book.tex | book-rules.mdc |"
  else
    echo "| Part count = 4 | FAIL ($part_count) | book.tex | Springer: 4 parts |"
  fi

  # 2. No subparts
  subparts=$({ grep -rc "^\\\\subpart{" ch*.tex book.tex 2>/dev/null || true; } | awk -F: '{s+=$2} END {print s+0}')
  if [ "$subparts" = "0" ]; then
    echo "| No subparts | PASS | — | Springer: subparts forbidden |"
  else
    echo "| No subparts | FAIL ($subparts) | chapters | Springer: subparts forbidden |"
  fi

  # 3. Chapter skeleton
  for f in ch*.tex; do
    [ -f "$f" ] || continue
    has_label=$(grep -c "^\\\\label{ch:" "$f" 2>/dev/null || true)
    has_label=${has_label:-0}
    has_refseg=$(grep -c "^\\\\newrefsegment" "$f" 2>/dev/null || true)
    has_refseg=${has_refseg:-0}
    if [ "$has_label" -ge 1 ]; then
      echo "| Chapter label | PASS | $f | book-rules.mdc |"
    else
      echo "| Chapter label | FAIL | $f | book-rules.mdc |"
    fi
    if [ "$has_refseg" -ge 1 ]; then
      echo "| \\\\newrefsegment | PASS | $f | biblatex refsegment=chapter |"
    else
      echo "| \\\\newrefsegment | FAIL | $f | biblatex refsegment=chapter |"
    fi
  done

  # 4. Abstract word counts
  for f in ch*.tex; do
    [ -f "$f" ] || continue
    count=$(awk '/\\abstract\*?\{/,/\}$/' "$f" 2>/dev/null \
      | tr -d '\n' \
      | sed 's/\\abstract\*\?{//' \
      | sed 's/}[^}]*$//' \
      | wc -w)
    if [ "$count" -le 200 ] && [ "$count" -gt 0 ]; then
      echo "| Abstract ≤ 200 words | PASS | $f ($count) | Springer: ≤ 200 words |"
    elif [ "$count" -eq 0 ]; then
      echo "| Abstract present | FAIL | $f | Springer: abstract required |"
    else
      echo "| Abstract ≤ 200 words | FAIL | $f ($count) | Springer: ≤ 200 words |"
    fi
  done

  # 5. Front matter stubs
  for stub in dedication foreword preface acknowledgement glossary acronym; do
    f="author/${stub}.tex"
    if [ -f "$f" ]; then
      lines=$(wc -l < "$f" | tr -d ' ')
      if [ "$lines" -gt 3 ]; then
        echo "| Front matter: $stub | PASS | $f ($lines lines) | Springer front matter |"
      else
        echo "| Front matter: $stub | WARN | $f ($lines lines) | Fill before submission |"
      fi
    else
      echo "| Front matter: $stub | FAIL | $f missing | Springer front matter |"
    fi
  done

  # 6. LLM-use declaration
  ack="author/acknowledgement.tex"
  if [ -f "$ack" ] && grep -qiE "LLM|large language model|generative AI|Claude|GPT|artificial intelligence" "$ack"; then
    echo "| AI/LLM use declared | PASS | $ack | Springer: LLM use must be declared |"
  else
    echo "| AI/LLM use declared | MANUAL | $ack | Springer: declare if any AI used |"
  fi

} > "$OUT"

echo "Report written to $OUT"
