#!/bin/bash

# Script to safely pull latest changes from base repository
# This ensures you're not accidentally running it from within the base repo itself

set -e

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Get the origin remote URL
ORIGIN_URL=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$ORIGIN_URL" ]; then
    echo "Error: No origin remote found"
    exit 1
fi

# Check if this is the base repository (katha-base)
if echo "$ORIGIN_URL" | grep -q "katha-base"; then
    echo "=========================================="
    echo "ERROR: You are in the base repository!"
    echo "=========================================="
    echo ""
    echo "This script is meant to pull changes FROM base,"
    echo "not to be run IN the base repository itself."
    echo ""
    echo "Please run this script from a forked repository."
    echo "=========================================="
    exit 1
fi

# Check if base remote exists, if not add it
if ! git remote get-url base > /dev/null 2>&1; then
    echo "Adding 'base' remote..."
    git remote add base https://github.com/treuille/katha-base.git
    echo "✓ Added base remote: https://github.com/treuille/katha-base.git"
    echo ""
fi

echo "Fetching all remotes..."
git fetch --all

echo ""
echo "Pulling from base/main..."
git pull base main

echo ""
echo "✓ Successfully updated from base!"
