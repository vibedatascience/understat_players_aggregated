#!/bin/bash

# Daily git push script for understat data
# This script commits and pushes updated data files to GitHub

# Change to the correct directory
cd /Users/rchaudhary/Downloads/understat_data

# Set up logging
LOG_FILE="git_push_cron.log"
echo "$(date): Starting daily git push" >> "$LOG_FILE"

# Check if there are any changes to commit
if git diff --quiet && git diff --cached --quiet; then
    echo "$(date): No changes to commit" >> "$LOG_FILE"
    exit 0
fi

# Add all changed files
git add . >> "$LOG_FILE" 2>&1

# Create commit with timestamp
COMMIT_MSG="Daily data update - $(date +'%Y-%m-%d %H:%M')

Updated latest season data and combined datasets

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git commit -m "$COMMIT_MSG" >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): Commit successful" >> "$LOG_FILE"
    
    # Push to GitHub
    git push >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "$(date): Push successful" >> "$LOG_FILE"
    else
        echo "$(date): Push failed" >> "$LOG_FILE"
        exit 1
    fi
else
    echo "$(date): Commit failed" >> "$LOG_FILE"
    exit 1
fi

echo "$(date): Daily git push completed successfully" >> "$LOG_FILE"