# advanced_llm_ops_cursor_v2

Workspace: `advanced_llm_ops_cursor_v2`

make audit                    # full compliance audit, updates LATEST_SUMMARY.md
make audit-quick              # structure + float only (~10s)
make compliance-baseline      # freeze current state as new baseline
make build                    # latexmk -pdf book.tex
make clean                    # latexmk -C