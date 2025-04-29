#!/bin/bash

# Prompt for commit message
echo "Enter a commit message:"
read msg

# Stage all changes
git add .

# Commit with message
git commit -m "$msg"

# Push to GitHub
git push

echo "✅ Code pushed to GitHub and Render will redeploy shortly!"
