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
1. Show me what files are staged vs unstaged
2. If there are unstaged changes, ask which files to add
3. Analyze the staged changes and suggest a descriptive commit message
4. Ask if I want to use your suggested message or provide my own
5. Commit with the approved message including:

   Co-Authored-By: Claude <noreply@anthropic.com>
6. Show what was committed
