#!/bin/bash

# Overleaf Git Sync Script
# This script syncs your local repository to Overleaf via Git

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if overleaf remote exists
if ! git remote | grep -q "^overleaf$"; then
    echo -e "${RED}Error: Overleaf remote not configured.${NC}"
    echo ""
    echo "To set up Overleaf Git sync:"
    echo "1. Go to your Overleaf project"
    echo "2. Click 'Menu' → 'Git'"
    echo "3. Copy the Git URL (e.g., https://git.overleaf.com/xxxxx)"
    echo "4. Run: git remote add overleaf <URL>"
    echo ""
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

echo -e "${YELLOW}Syncing to Overleaf...${NC}"
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}Warning: You have uncommitted changes.${NC}"
    echo "Consider committing them first with: git add . && git commit -m 'Update'"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Push to Overleaf
echo -e "${YELLOW}Pushing to Overleaf...${NC}"
if git push overleaf "$CURRENT_BRANCH"; then
    echo -e "${GREEN}✓ Successfully synced to Overleaf!${NC}"
    echo ""
    echo "Your changes should now be visible in Overleaf."
    echo "Note: Overleaf may take a few seconds to update."
else
    echo -e "${RED}✗ Failed to sync to Overleaf${NC}"
    echo ""
    echo "Common issues:"
    echo "- Make sure you're authenticated (check Overleaf Git URL)"
    echo "- Ensure your branch exists on Overleaf"
    echo "- Try: git push overleaf $CURRENT_BRANCH --force (if you need to overwrite)"
    exit 1
fi

