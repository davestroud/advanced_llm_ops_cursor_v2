# Automatic Overleaf Sync Setup Guide

This guide explains how to set up automatic syncing between your local repository and Overleaf using Git.

---

## Overview

Overleaf supports Git integration, which allows you to automatically sync your local changes to Overleaf without manual uploads. This is the recommended method for keeping your Overleaf project up-to-date.

---

## Prerequisites

- Git repository initialized (✓ Already done)
- Overleaf account and project created
- Git credentials configured (if using HTTPS)

---

## Setup Instructions

### Step 1: Get Your Overleaf Git URL

1. Open your Overleaf project in a web browser
2. Click the **"Menu"** button (☰) in the top-left corner
3. Select **"Git"** from the dropdown menu
4. Copy the Git URL shown (e.g., `https://git.overleaf.com/xxxxx` or `git@git.overleaf.com:xxxxx`)

**Note:** If you don't see the Git option, you may need to:
- Upgrade your Overleaf plan (Git is available on paid plans)
- Or use the manual sync script instead (see Alternative Method below)

### Step 2: Add Overleaf as a Git Remote

Run this command in your project directory, replacing `<OVERLEAF_URL>` with the URL you copied:

```bash
git remote add overleaf <OVERLEAF_URL>
```

**Example:**
```bash
git remote add overleaf https://git.overleaf.com/1234567890abcdef
```

Verify the remote was added:
```bash
git remote -v
```

You should see both `origin` (GitHub) and `overleaf` remotes.

### Step 3: Initial Sync to Overleaf

For the first sync, you may need to push your current branch:

```bash
git push overleaf main
```

If Overleaf has a different branch name or structure, you may need to:
```bash
git push overleaf main:master  # If Overleaf uses 'master' branch
```

---

## Usage Methods

### Method 1: Manual Sync Script (Recommended for Control)

Use the provided `sync-overleaf.sh` script whenever you want to sync:

```bash
./sync-overleaf.sh
```

**Make the script executable:**
```bash
chmod +x sync-overleaf.sh
```

This script will:
- Check if Overleaf remote is configured
- Warn about uncommitted changes
- Push your current branch to Overleaf
- Provide helpful error messages

### Method 2: Automatic Sync on Commit (Recommended for Convenience)

The repository includes a Git post-commit hook that automatically syncs to Overleaf after every commit.

**Enable the hook:**
```bash
chmod +x .git/hooks/post-commit
```

Now, every time you commit:
```bash
git add .
git commit -m "Your commit message"
```

The changes will automatically be pushed to Overleaf in the background.

**Disable automatic sync:**
```bash
chmod -x .git/hooks/post-commit
# Or rename it:
mv .git/hooks/post-commit .git/hooks/post-commit.disabled
```

### Method 3: Manual Git Push

You can also push directly using Git:

```bash
git push overleaf main
```

Or push all branches:
```bash
git push overleaf --all
```

---

## Workflow Recommendations

### Recommended Workflow

1. **Make changes locally** in your LaTeX files
2. **Test compilation locally** (if you have LaTeX installed)
3. **Commit changes:**
   ```bash
   git add .
   git commit -m "Update chapter X"
   ```
4. **Sync to Overleaf:**
   - If using automatic hook: Already done!
   - If using manual script: `./sync-overleaf.sh`
   - If using manual push: `git push overleaf main`
5. **Verify in Overleaf:** Check that changes appear correctly

### Branch Strategy

- **Main branch:** Keep `main` branch synced with Overleaf
- **Feature branches:** Create branches for major edits, merge to `main` when ready
- **Overleaf branch:** Typically sync `main` to Overleaf's `main` or `master` branch

---

## Troubleshooting

### Error: "remote 'overleaf' already exists"

If you've already added the remote, you can update it:
```bash
git remote set-url overleaf <NEW_OVERLEAF_URL>
```

Or remove and re-add:
```bash
git remote remove overleaf
git remote add overleaf <OVERLEAF_URL>
```

### Error: Authentication Failed

**For HTTPS URLs:**
- Overleaf may require a personal access token
- Go to Overleaf → Account Settings → Git → Generate Token
- Use the token as your password when Git prompts

**For SSH URLs:**
- Ensure your SSH key is added to Overleaf
- Go to Overleaf → Account Settings → SSH Keys

### Error: "Updates were rejected"

This usually means Overleaf has changes you don't have locally. Options:

1. **Pull from Overleaf first** (if you made changes in Overleaf):
   ```bash
   git pull overleaf main --no-rebase
   ```

2. **Force push** (⚠️ **Warning:** This overwrites Overleaf's changes):
   ```bash
   git push overleaf main --force
   ```

### Sync Script Not Working

1. **Check if script is executable:**
   ```bash
   ls -l sync-overleaf.sh
   chmod +x sync-overleaf.sh
   ```

2. **Check if Overleaf remote exists:**
   ```bash
   git remote -v
   ```

3. **Run script with bash explicitly:**
   ```bash
   bash sync-overleaf.sh
   ```

### Post-Commit Hook Not Running

1. **Check if hook is executable:**
   ```bash
   ls -l .git/hooks/post-commit
   chmod +x .git/hooks/post-commit
   ```

2. **Test the hook manually:**
   ```bash
   .git/hooks/post-commit
   ```

3. **Check Git hook configuration:**
   ```bash
   git config core.hooksPath
   ```

---

## File Filtering

The Git sync will push all committed files. To exclude build artifacts, ensure you have a `.gitignore` file. Create one if needed:

```bash
# LaTeX build artifacts
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.log
*.pdf
*.run.xml
*.synctex.gz
*.toc
*.idx
*.ilg
*.ind

# Overleaf-specific
overleaf-upload.zip
```

---

## Alternative: Manual Upload Script

If Git integration is not available, you can create a script to manually upload files. However, Git sync is strongly recommended as it's more reliable and preserves history.

---

## Best Practices

1. **Commit frequently:** Small, logical commits make syncing easier
2. **Test locally first:** Compile locally before syncing to catch errors early
3. **Use meaningful commit messages:** Helps track changes in Overleaf history
4. **Keep Overleaf as read-only:** Make all edits locally, sync to Overleaf
5. **Backup regularly:** Your GitHub remote serves as a backup

---

## Quick Reference

```bash
# Add Overleaf remote
git remote add overleaf <OVERLEAF_URL>

# Sync manually
./sync-overleaf.sh

# Sync via Git
git push overleaf main

# Check remotes
git remote -v

# Update Overleaf URL
git remote set-url overleaf <NEW_URL>

# Remove Overleaf remote
git remote remove overleaf
```

---

## Success Indicators

✅ Overleaf remote configured (`git remote -v` shows `overleaf`)  
✅ Sync script runs without errors  
✅ Changes appear in Overleaf within a few seconds  
✅ No build artifacts synced (check `.gitignore`)  

---

## Need Help?

- **Overleaf Git Documentation:** https://www.overleaf.com/learn/how-to/Using_Git_and_GitHub
- **Git Basics:** https://git-scm.com/doc
- **Check your Overleaf project:** Look for the Git menu option

---

**Last Updated:** $(date)

