---
description: Commit current changes with an AI-suggested message
allowed-tools: Bash(git status:*), Bash(git add:*), Bash(git commit:*), Bash(git diff:*)
---

Analyze the current git changes and help me commit them.

Current status:
!`git status`

Changes to be committed:
!`git diff --cached`

Unstaged changes:
!`git diff`

Please:
1. Show me clearly what files are staged vs unstaged
2. If there are unstaged changes, ask me which files to add:
   - Add all unstaged files
   - Add specific files (let me specify which ones)
   - Commit only what's already staged
3. After staging is finalized, analyze ALL the staged changes and suggest a descriptive commit message that follows best practices
4. Ask me if I want to use your suggested message or provide my own
5. Once I approve, commit the staged changes with the final message
6. Show me a summary of what was committed
