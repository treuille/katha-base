---
description: Go back one commit (keeps changes staged)
allowed-tools: Bash(git log:*), Bash(git reset:*), Bash(git diff:*)
---

Go back one commit in time, keeping all changes staged.

Current commit:
!`git log -1 --oneline`

Commit we're moving back from:
!`git log -1 --format='%h - %s (%ar)'`

Please:
1. Execute `git reset --soft HEAD~1` to go back one commit
2. Show me the commit message that was just undone
3. Show me what changes are now staged (using `git diff --cached`)
4. Summarize what changed and what state the repository is now in
