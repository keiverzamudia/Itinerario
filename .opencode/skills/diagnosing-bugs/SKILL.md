---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
---

# Diagnosing Bugs

A discipline for hard bugs. Skip phases only when explicitly justified.

## Phase 1: Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug, you will find the cause.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one

1. **Failing test** at whatever seam reaches the bug
2. **Curl / HTTP script** against a running dev server
3. **CLI invocation** with a fixture input
4. **Headless browser script** (Playwright) that drives the UI and asserts on DOM/console/network
5. **Replay a captured trace**
6. **Throwaway harness** — minimal subset that exercises the bug
7. **Property / fuzz loop** — run 1000 random inputs
8. **Bisection harness** — automate `git bisect run`
9. **Differential loop** — same input, old vs new, diff outputs

### Tighten the loop

- Can I make it faster?
- Can I make the signal sharper?
- Can I make it more deterministic?

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is a debugging superpower.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for access, artifacts, or permission to add instrumentation. **Do not proceed to hypothesise without a loop.**

## Phase 2: Reproduce + minimise

Run the loop. Confirm:

- [ ] The loop produces the failure mode the **user** described
- [ ] The failure is reproducible across multiple runs
- [ ] You have captured the exact symptom

### Minimise

Shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**. Keep only what's load-bearing.

Done when **every remaining element is load-bearing**.

## Phase 3: Hypothesise

Generate **3–5 ranked hypotheses** before testing any. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**:

> "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly.

## Phase 4: Instrument

Each probe maps to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:
1. **Debugger / REPL inspection** if available
2. **Targeted logs** at boundaries that distinguish hypotheses
3. Never "log everything and grep"

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup = single grep.

## Phase 5: Fix + regression test

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam exercises the **real bug pattern** at the call site. If no correct seam exists, that itself is the finding — flag it.

If a correct seam exists:
1. Turn minimised repro into failing test
2. Watch it fail
3. Apply the fix
4. Watch it pass
5. Re-run Phase 1 loop against original scenario

## Phase 6: Cleanup

Required before declaring done:

- [ ] Original repro no longer reproduces
- [ ] Regression test passes (or absence of seam documented)
- [ ] All `[DEBUG-...]` instrumentation removed
- [ ] Throwaway prototypes deleted
- [ ] The correct hypothesis is stated in commit message
