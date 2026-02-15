# Overleaf Upload Checklist

Use this checklist to ensure all files are uploaded correctly to Overleaf.

---

## Pre-Upload Preparation

- [ ] Create a new project in Overleaf (or use existing project)
- [ ] Note: Overleaf will automatically generate build artifacts (`.aux`, `.log`, `.pdf`, etc.) - do not upload these

---

## Step 1: Upload Root Files (5 files)

Upload these files directly to the project root:

- [ ] `SNmono.cls` - Springer Nature monograph class file (CRITICAL - must be in root)
- [ ] `svind.ist` - Index style file
- [ ] `macros.tex` - Custom LaTeX macros
- [ ] `references.bib` - Bibliography database
- [ ] `book.tex` - Main document file (upload last, or set as main document after upload)

**Verification:** All 5 files should appear in the root directory listing.

---

## Step 2: Create Author Directory and Upload Files (11 files)

1. Create `author/` folder in Overleaf:
   - [ ] Click "New Folder" in Overleaf
   - [ ] Name it `author` (lowercase)

2. Upload these files to `author/` folder:

   **Front Matter:**
   - [ ] `author/dedication.tex`
   - [ ] `author/foreword.tex`
   - [ ] `author/preface.tex`
   - [ ] `author/acknowledgement.tex`

   **Part Introductions:**
   - [ ] `author/part1-foundations.tex`
   - [ ] `author/part2-delivery.tex`
   - [ ] `author/part3-optimization.tex`
   - [ ] `author/part4-governance.tex`

   **Back Matter:**
   - [ ] `author/acronym.tex`
   - [ ] `author/appendix.tex`
   - [ ] `author/glossary.tex`

**Verification:** The `author/` folder should contain exactly 11 `.tex` files.

---

## Step 3: Upload Chapter Files (12 files)

Upload all chapter files to the project root:

- [ ] `ch01-intro-ishar.tex`
- [ ] `ch02-llmops-fundamentals.tex`
- [ ] `ch03-infra-env.tex`
- [ ] `ch04-cicd.tex`
- [ ] `ch05-observability.tex`
- [ ] `ch06-scaling.tex`
- [ ] `ch07-performance.tex`
- [ ] `ch08-rag.tex`
- [ ] `ch09-agents-orchestration.tex`
- [ ] `ch10-testing-eval.tex`
- [ ] `ch11-ethics.tex`
- [ ] `ch12-ishtar-end-to-end.tex`

**Verification:** All 12 chapter files should appear in the root directory listing.

---

## Step 4: Configure Overleaf Settings

### Set Main Document
- [ ] Click the menu button (☰) next to "Recompile" button
- [ ] Select "Main document"
- [ ] Choose `book.tex` from the dropdown
- [ ] Click "Set as Main Document"

### Compiler Settings
- [ ] Click "Menu" → "Settings" (or "Compiler" dropdown)
- [ ] Set **Compiler** to: `pdfLaTeX`
- [ ] Set **Bibliography** to: `Biber` (NOT BibTeX)
- [ ] Set **Main document** to: `book.tex`

### Compilation Sequence
Overleaf should automatically run:
1. pdfLaTeX
2. Biber (for bibliography)
3. pdfLaTeX (x2 for cross-references)

**Note:** First compilation may take longer. Subsequent compilations will be faster.

---

## Step 5: Post-Upload Verification

### File Structure Check
- [ ] Root directory contains exactly 17 files:
  - 5 root files (`book.tex`, `SNmono.cls`, `svind.ist`, `macros.tex`, `references.bib`)
  - 12 chapter files (`ch01-*.tex` through `ch12-*.tex`)
- [ ] `author/` folder exists and contains exactly 11 `.tex` files
- [ ] No `.aux`, `.log`, `.bbl`, `.pdf`, or other build artifacts were uploaded

### Compilation Check
- [ ] Click "Recompile" button
- [ ] Wait for compilation to complete
- [ ] Check for errors in the log:
  - ✅ **Success:** PDF generated without errors
  - ⚠️ **Warnings:** May appear (check if critical)
  - ❌ **Errors:** Must be resolved (see Troubleshooting below)

### Content Verification
- [ ] PDF opens and displays correctly
- [ ] Table of contents is present
- [ ] All 12 chapters appear in the PDF
- [ ] Bibliography appears at the end of each chapter (chapter-local references)
- [ ] Index appears at the end (if entries exist)
- [ ] No missing file errors in the log

---

## Troubleshooting

### Error: "File `SNmono.cls' not found"
- **Solution:** Ensure `SNmono.cls` is uploaded to the root directory (not in a subfolder)
- **Check:** File should appear at the same level as `book.tex`

### Error: "File `author/XXX.tex' not found"
- **Solution:** Verify the `author/` folder exists and contains the referenced file
- **Check:** File names must match exactly (case-sensitive)

### Error: "File `chXX-XXX.tex' not found"
- **Solution:** Verify all 12 chapter files are in the root directory
- **Check:** File names must match exactly what's in `book.tex` (e.g., `ch01-intro-ishar.tex`)

### Error: "Bibliography file `references.bib' not found"
- **Solution:** Ensure `references.bib` is in the root directory
- **Check:** File should appear at the same level as `book.tex`

### Error: "Biber error" or bibliography not working
- **Solution:** Verify compiler settings:
  - Compiler: `pdfLaTeX`
  - Bibliography: `Biber` (NOT BibTeX)
- **Check:** Recompile multiple times (pdfLaTeX → Biber → pdfLaTeX → pdfLaTeX)

### Warning: "Label `XXX' multiply defined"
- **Solution:** This indicates duplicate `\label{}` commands. Check the source files for duplicate labels.
- **Note:** Some warnings may be acceptable, but errors must be resolved.

### PDF only shows 22 pages (or stops early)
- **Solution:** This usually indicates a fatal compilation error. Check the log for:
  - Missing files
  - Syntax errors in `.tex` files
  - Missing `\end{document}` or unmatched braces
- **Check:** Look for the first error in the log and resolve it

---

## Quick Reference

### Total Files to Upload: 28
- **Root:** 5 files
- **Chapters:** 12 files
- **Author folder:** 11 files

### Overleaf Settings
- **Compiler:** pdfLaTeX
- **Bibliography:** Biber
- **Main document:** book.tex

### File Structure
```
project-root/
├── book.tex
├── SNmono.cls
├── svind.ist
├── macros.tex
├── references.bib
├── ch01-intro-ishar.tex
├── ch02-llmops-fundamentals.tex
├── ... (ch03 through ch12)
└── author/
    ├── dedication.tex
    ├── foreword.tex
    ├── ... (all 11 author files)
```

---

## Additional Notes

- **Images:** If you have image files, create an `images/` folder and upload them there. Currently, all images are commented out in the source, so no images are required.
- **Build Artifacts:** Overleaf will automatically generate `.aux`, `.log`, `.bbl`, `.pdf`, etc. Do not upload these files - they will be regenerated.
- **First Compilation:** The first compilation may take 30-60 seconds. Subsequent compilations will be faster.
- **Chapter-Local Bibliographies:** Each chapter has its own bibliography section. This is intentional and configured via `biblatex` with `refsegment=chapter`.

---

## Success Criteria

✅ All 28 files uploaded  
✅ `book.tex` set as main document  
✅ Compiler set to pdfLaTeX  
✅ Bibliography set to Biber  
✅ PDF compiles without errors  
✅ All chapters visible in PDF  
✅ Table of contents present  
✅ Bibliographies appear at end of each chapter  

If all criteria are met, your upload is complete! 🎉
