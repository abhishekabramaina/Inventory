---
name: lint-pr
description: Lint a pull request for code quality issues
argument-hint: "[pr-number]"
arguments: [pr_number]
disable-model-invocation: true
allowed-tools: Read Grep Bash(git diff *)
---

## Lint PR #$pr_number

!`git diff origin/main...HEAD`

## Instructions

Review the diff above for:
- Code style violations
- Potential bugs or logic errors
- Missing error handling
- Hardcoded values that should be constants
- Tests that need updating
- Performance issues
- Security concerns

Format your findings as:
1. **Summary**: Overall quality assessment
2. **Issues**: List each issue with file, line, and severity
3. **Suggestions**: Recommended fixes

If no issues found, say the PR looks good.