# Investigation Plan: Float Placement Issues in Chapter 8

## Problem Statement
All tables (8.1-8.6) and figures (8.2, 8.3) are rendering at the end of Chapter 8, despite being positioned correctly in the source file near their relevant content sections.

## Root Cause Hypotheses

### Hypothesis 1: Too Many Floats Competing for Space
- **Check**: Count total floats in Chapter 8
- **Investigation**: 
  - Count all `\begin{table}` and `\begin{figure}` instances
  - Check if LaTeX's float queue is full (max 18 floats per page typically)
  - Verify if other chapters have similar float density

### Hypothesis 2: Tables/Figures Too Large for Page
- **Check**: Measure actual size of each table/figure
- **Investigation**:
  - Check table widths (should be ≤ 0.95\linewidth)
  - Check figure dimensions
  - Look for "Float too large" warnings in linter output
  - Verify if tables exceed page height limits

### Hypothesis 3: Insufficient Text Between Floats
- **Check**: Measure text content between floats
- **Investigation**:
  - Count lines of text between consecutive floats
  - LaTeX needs sufficient text to justify placing floats
  - Check if sections are too short

### Hypothesis 4: Float Placement Option Issues
- **Check**: Current placement options
- **Investigation**:
  - All currently use `[t]` (top only)
  - Rules allow `[tb]` (top or bottom) if needed
  - Consider if `[tb]` would help placement
  - Check if `[H]` is needed (rules say "unless absolutely required")

### Hypothesis 5: Missing References in Text
- **Check**: Are floats referenced near their placement?
- **Investigation**:
  - LaTeX tries to place floats near their references
  - Check if all tables/figures are referenced in prose
  - Verify references are within ±1 paragraph of float location

### Hypothesis 6: Section/Page Break Issues
- **Check**: Section breaks and page breaks
- **Investigation**:
  - Check for `\clearpage`, `\newpage` commands
  - Verify section structure doesn't force floats to end
  - Check if `\FloatBarrier` from `placeins` package is needed

## Investigation Steps

### Step 1: Count and Map All Floats
```bash
# Count total floats in chapter 8
grep -c "\\begin{table}" ch08-rag.tex
grep -c "\\begin{figure}" ch08-rag.tex

# Map float positions
grep -n "\\begin{table}\|\\begin{figure}" ch08-rag.tex
```

### Step 2: Check Float Sizes
- Review each table's width specification
- Check for "Float too large" linter warnings
- Measure figure dimensions in TikZ code

### Step 3: Check Text Density
- Count lines between floats
- Verify sufficient prose content exists
- Check if sections are too short

### Step 4: Check References
- Verify each float is referenced in text
- Check reference proximity to float location
- Ensure references use correct format (Table~\ref{}, Fig.~\ref{})

### Step 5: Review Placement Options
- Current: All use `[t]`
- Consider: Change to `[tb]` for better placement flexibility
- Last resort: Use `[H]` with `\usepackage{float}` if absolutely needed

### Step 6: Check for Float Barriers
- Check if `placeins` package is loaded
- Consider adding `\FloatBarrier` before section breaks
- Verify no `\clearpage` commands are interfering

## Expected Findings

### Most Likely Causes (in order):
1. **Too many floats** - Chapter 8 has 9 floats total, which may overwhelm LaTeX's float queue
2. **Large table sizes** - Some tables may be too wide/tall for available space
3. **Insufficient text** - Not enough prose between floats for LaTeX to place them
4. **Missing references** - Floats not referenced, so LaTeX defers placement

## Proposed Solutions (Priority Order)

### Solution 1: Add Float Barriers (Low Risk)
- Add `\usepackage{placeins}` to preamble
- Insert `\FloatBarrier` before major section breaks
- This forces LaTeX to place floats before moving to next section

### Solution 2: Change Placement to [tb] (Low Risk)
- Change `[t]` to `[tb]` for tables/figures that are floating
- Allows LaTeX more flexibility in placement
- Still complies with rules (rules allow `[tb]`)

### Solution 3: Split Large Tables (Medium Risk)
- If tables are too large, split into multiple smaller tables
- Or use landscape orientation for very wide tables
- Or reduce font size slightly (but maintain readability)

### Solution 4: Add More Text (Low Risk)
- Add brief introductory text before floats
- Ensure sufficient prose exists between floats
- LaTeX needs text to "anchor" float placement

### Solution 5: Use [H] Placement (Last Resort)
- Only if absolutely necessary
- Requires `\usepackage{float}`
- Rules say "avoid [H] floats unless absolutely required"
- This would force exact placement but may cause page breaks

### Solution 6: Reference All Floats (Best Practice)
- Add references to all tables/figures in prose
- Place references within ±1 paragraph of float location
- LaTeX uses references to guide placement

## Implementation Order

1. **First**: Check float counts and sizes (Steps 1-2)
2. **Second**: Add references if missing (Step 4)
3. **Third**: Try `[tb]` placement option (Step 5)
4. **Fourth**: Add `\FloatBarrier` if needed (Step 6)
5. **Last**: Consider `[H]` or table splitting if above don't work

## Success Criteria

- All tables/figures appear near their relevant content (within same section)
- No floats appear at end of chapter
- No "Float too large" warnings
- All floats properly referenced in text
- Document compiles without errors

## Files to Check

- `ch08-rag.tex` - Main chapter file
- `book.tex` - Check if `placeins` package is loaded
- `macros.tex` - Check for any float-related macros
- Linter output - Check for float-related warnings
