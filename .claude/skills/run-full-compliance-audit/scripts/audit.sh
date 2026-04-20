#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
OUT="docs/audit_reports/FULL_AUDIT_${TIMESTAMP}.md"
SUMMARY="docs/audit_reports/LATEST_SUMMARY.md"
mkdir -p docs/audit_reports

# Ordered list; bash-3 compatible (no associative arrays).
SKILLS="springer-structure-audit springer-float-audit springer-typography-audit springer-citation-audit springer-cross-ref-audit springer-accessibility-audit springer-ai-declaration-audit"

skill_prefix() {
  case "$1" in
    springer-structure-audit)      echo "structure_" ;;
    springer-float-audit)          echo "floats_" ;;
    springer-typography-audit)     echo "typography_" ;;
    springer-citation-audit)       echo "citations_" ;;
    springer-cross-ref-audit)      echo "cross_refs_" ;;
    springer-accessibility-audit)  echo "accessibility_" ;;
    springer-ai-declaration-audit) echo "ai_declaration_" ;;
  esac
}

# Run each skill
for skill in $SKILLS; do
  echo "Running $skill..."
  bash ".claude/skills/${skill}/scripts/audit.sh" > /dev/null
done

# Header + executive summary
{
  echo "# Full Springer Compliance Audit — $TIMESTAMP"
  echo ""
  echo "## Executive summary"
  echo ""
  echo "| Skill | PASS | FAIL | WARN | MANUAL |"
  echo "|-------|------|------|------|--------|"

  for skill in $SKILLS; do
    prefix=$(skill_prefix "$skill")
    latest=$(ls -1t docs/audit_reports/ 2>/dev/null | grep "^${prefix}" | head -1 || true)
    if [ -n "$latest" ] && [ -f "docs/audit_reports/$latest" ]; then
      report="docs/audit_reports/$latest"
      pass=$(grep -cE "(\| PASS |^PASS )" "$report" 2>/dev/null || true);          pass=${pass:-0}
      fail=$(grep -cE "(\| FAIL |^FAIL )" "$report" 2>/dev/null || true);          fail=${fail:-0}
      warn=$(grep -cE "(\| WARN |^WARN |— WARN)" "$report" 2>/dev/null || true);   warn=${warn:-0}
      manual=$(grep -cE "(\| MANUAL |MANUAL REVIEW)" "$report" 2>/dev/null || true); manual=${manual:-0}
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
  for skill in $SKILLS; do
    prefix=$(skill_prefix "$skill")
    latest=$(ls -1t docs/audit_reports/ 2>/dev/null | grep "^${prefix}" | head -1 || true)
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
