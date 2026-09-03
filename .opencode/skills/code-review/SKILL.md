---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to 'review since X'."
---

# Code Review

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot). Also note commits via `git log <fixed-point>..HEAD --oneline`.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in commit messages (`#123`, `Closes #45`)
2. A path the user passed as an argument
3. A spec file under `docs/` or `specs/`
4. If nothing found, ask the user. No spec = Standards-only review.

### 3. Identify standards sources

Anything in the repo that documents how code should be written, plus the **smell baseline** (Fowler code smells):

- **Mysterious Name**: name doesn't reveal what it does → rename
- **Duplicated Code**: same logic in multiple places → extract
- **Feature Envy**: method reaches into another object's data → move it
- **Data Clumps**: same fields travel together → bundle into type
- **Primitive Obsession**: primitive standing in for domain concept → give it its own type
- **Shotgun Surgery**: one change forces edits across many files → gather together
- **Divergent Change**: one file edited for unrelated reasons → split
- **Speculative Generality**: abstraction for needs that don't exist → delete

### 4. Review both axes

**Standards axis:** Check for:
- Code smells from the baseline above
- Naming conventions
- Error handling patterns
- Security practices (parameterized queries, input validation)
- Test coverage of new code

**Spec axis:** Check for:
- Requirements from the spec that are missing or partial
- Behavior not asked for (scope creep)
- Requirements that look implemented but are wrong

### 5. Report

Present findings under `## Standards` and `## Spec` headings. Do not merge or rerank — the two axes are deliberately separate. A change can pass one axis and fail the other.

End with: total findings per axis, and the worst issue within each.
