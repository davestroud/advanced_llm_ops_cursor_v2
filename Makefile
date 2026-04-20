.PHONY: audit audit-quick compliance-baseline build clean

build:
	@latexmk -pdf book.tex

clean:
	@latexmk -C

audit:
	@bash .claude/skills/run-full-compliance-audit/scripts/audit.sh

audit-quick:
	@bash .claude/skills/springer-structure-audit/scripts/audit.sh
	@bash .claude/skills/springer-float-audit/scripts/audit.sh
	@echo "Quick audit done. Full audit: make audit"

compliance-baseline:
	@echo "Capturing current compliance as baseline..."
	@bash .claude/skills/run-full-compliance-audit/scripts/audit.sh
	@cp docs/audit_reports/LATEST_SUMMARY.md \
	    docs/audit_reports/BASELINE_SUMMARY.md
	@echo "Baseline saved to docs/audit_reports/BASELINE_SUMMARY.md"
