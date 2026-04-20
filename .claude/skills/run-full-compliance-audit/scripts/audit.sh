#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="docs/audit_reports/FULL_AUDIT_${TIMESTAMP}.md"
SUMMARY="docs/audit_reports/LATEST_SUMMARY.md"
mkdir -p docs/audit_reports

SKILLS=(
  springer-structure-audit
  springer-float-audit
  springer-typography-audit
  springer-citation-audit
  springer-cross-ref-audit
  springer-accessibility-audit
  springer-ai-declaration-audit
)

# Run each skill
declare -A LATEST_REPORT
for skill in "${SKILLS[@]}"; do
  echo "Running $skill..."
  bash ".claude/skills/${skill}/scripts/audit.sh" > /dev/null
  keyword=$(echo "$skill" | sed 's/springer-//;s/-audit//' | sed 's/-/_/g')
  # Map skill names to report file prefixes
  case "$skill" in
    springer-structure-audit)      prefix="structure_" ;;
    springer-float-audit)          prefix="floats_" ;;
    springer-typography-audit)     prefix="typography_" ;;
    springer-citation-audit)       prefix="citations_" ;;
    springer-cross-ref-audit)      prefix="cross_refs_" ;;
    springer-accessibility-audit)  prefix="accessibility_" ;;
    springer-ai-declaration-audit) prefix="ai_declaration_" ;;
  esac
  latest=$(ls -1t docs/audit_reports/ 2>/dev/null | grep "^${prefix}" | head -1 || true)
  LATEST_REPORT[$skill]="$latest"
done

# Header + executive summary
{
  echo "# Full Springer Compliance Audit — $TIMESTAMP"
  echo ""
  echo "## Executive summary"
  echo ""
  echo "| Skill | PASS | FAIL | WARN | MANUAL |"
  echo "|-------|------|------|------|--------|"

  for skill in "${SKILLS[@]}"; do
    latest="${LATEST_REPORT[$skill]}"
    if [ -n "$latest" ] && [ -f "docs/audit_reports/$latest" ]; then
      report="docs/audit_reports/$latest"
      pass=$(grep -cE "(\| PASS |^PASS )" "$report" 2>/dev/null || echo 0)
      fail=$(grep -cE "(\| FAIL |^FAIL )" "$report" 2>/dev/null || echo 0)
      warn=$(grep -cE "(\| WARN |^WARN |— WARN)" "$report" 2>/dev/null || echo 0)
      manual=$(grep -cE "(\| MANUAL |MANUAL REVIEW)" "$report" 2>/dev/null || echo 0)
      echo "| $skill | $pass | $fail | $warn | $manual |"
    else
      echo "| $skill | — | — | — | (no report) |"
    fi
  done
} > "$OUT"

# Append full detailed reports
{
  echo ""
  echo "## Detailed reports"
  for skill in "${SKILLS[@]}"; do
    latest="${LATEST_REPORT[$skill]}"
    if [ -n "$latest" ] && [ -f "docs/audit_reports/$latest" ]; then
      echo ""
      echo "---"
      echo ""
      cat "docs/audit_reports/$latest"
    fi
  done
} >> "$OUT"

# Extract summary-only file
sed -n '/^# Full Springer/,/^## Detailed reports/p' "$OUT" \
  | sed '$d' > "$SUMMARY"

echo ""
echo "Full report: $OUT"
echo "Summary:     $SUMMARY"
