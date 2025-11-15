---
description: Go forward one commit (undo last /back)
allowed-tools: Bash(git log:*), Bash(git reset:*), Bash(git diff:*), Bash(git reflog:*)
---

Go forward one step in time by undoing the last reset operation.

Current position:
!`git log -1 --oneline`

Reflog (recent HEAD positions):
!`git reflog -5 --format='%h %gd: %gs'`

Please:
1. Check the reflog to see if there's a position to move forward to
2. If there is, execute `git reset --soft HEAD@{1}` to go forward one step
3. Show me where we moved to (commit message)
4. Show me what changed (using `git diff` to show any unstaged changes, or explain the new state)
5. Summarize what state the repository is now in

Note: If there's no forward position available (we're already at the most recent position), let me know.
