# The Loop Playbook

A loop is an agent repeating cycles of work until a stop condition is met. This file is the routing table: which primitive fits which work, how to phrase a suggestion, and how to keep loops from eating tokens. The taxonomy follows the Claude Code team's published guidance on designing loops.

Start with the simplest primitive that fits. Most tasks need no loop at all.

## The four loop types

### 1. Turn-based (the default agentic loop)

- **Trigger:** a user prompt. **Stop:** Claude judges the task complete or needs input.
- **Best for:** shorter, one-off tasks; exploration; anything where the human should stay in the loop.
- **Upgrade path:** the human is usually the verification step. Encode that verification as a skill so the loop checks its own work end to end, the way a reviewer would:

```markdown
---
name: verify-frontend-change
description: Verify any UI change end-to-end before declaring it done.
---

# Verifying frontend changes

Never report a UI change as complete based on a successful edit alone.

1. Start the dev server and open the edited page in the browser.
2. Interact with the change directly: click the new control, confirm the state change, screenshot before and after.
3. Check the browser console: zero new errors or warnings.
4. Run a performance trace and audit Core Web Vitals.

If any step fails, fix the issue and rerun from step 1. Do not hand back partially verified work.
```

The more quantitative the checks, the more of the loop Claude can close itself.

### 2. Goal-based (`/goal`)

- **Trigger:** a manual prompt. **Stop:** the goal is met, or a turn cap is reached.
- **Best for:** tasks with verifiable exit criteria. Deterministic criteria work best: "all 143 tests pass", "Lighthouse score 90 or above", "zero type errors".
- **Always include a cap.** Example:

```
/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries
```

- When the user defines done, Claude stops judging "good enough" and stops stopping early. Vague goals produce loops that run long and quit early at the same time.

### 3. Time-based (`/loop`, `/schedule`)

- **Trigger:** an interval. **Stop:** cancelled, or the watched work completes (PR merges, queue empties).
- **Best for:** recurring work, or interfacing with external systems by polling them: CI, code review, deploys, queues.
- `/loop` runs on the local machine and dies with it; `/schedule` moves the routine to the cloud.
- Match the interval to how fast the watched thing actually changes. Example:

```
/loop 5m check my PR, address review comments, and fix failing CI
```

### 4. Proactive (composed)

- **Trigger:** an event or schedule, no human in real time. **Stop:** each task exits on its goal; the routine runs until switched off.
- **Best for:** recurring streams of well-defined work: bug triage, migrations, dependency upgrades, feedback queues.
- Composed from the other primitives: `/schedule` for the trigger, `/goal` for done, verification skills for quality, workflows for fan-out, auto mode for permissions. Example shape:

```
/schedule every hour: check the project-feedback channel for bug reports.
/goal: don't stop until every report found this run is triaged, actioned, and responded to.
When fixing a bug, use a workflow to explore three solutions in parallel worktrees
and have a judge adversarially review them.
```

## Making the suggestion

When a loop-radar signal fires (the table lives in SKILL.md), finish the current task first, then suggest. A good suggestion has four parts:

1. **The observation, specific.** "This is the third time this session you have asked me to check CI and fix what failed."
2. **The primitive and a ready-to-paste command**, filled in with the user's real project details, never placeholders.
3. **The stop condition and rough cost.** What ends it, how often it runs, and that each cycle spends tokens.
4. **An easy no.** "Happy to keep doing it manually instead."

Etiquette: one suggestion per task shape per session. A declined suggestion stays declined for the session. Never create a schedule, cron job, loop, or workflow without an explicit yes; the user owns their token budget and their crontab.

## Token discipline

- **Right-size the primitive.** No multi-agent workflow for work one turn can do; no loop for work one `/goal` can finish.
- **Success criteria first.** Specific done-criteria let the loop stop at the right moment instead of too late and too early.
- **Pilot fan-outs on a slice.** Workflows can spawn hundreds of agents; gauge cost on 5 items before running 500.
- **Scripts beat reasoning for deterministic steps.** Write the script once, have the loop run it each cycle instead of re-deriving the logic.
- **Interval matches reality.** Check CI every 5 minutes, not every 30 seconds. React to events instead of polling when an event source exists.
- **Review usage.** `/usage` breaks down spend, `/goal` with no arguments shows turns so far, `/workflows` shows per-agent usage and lets you stop drift.

## Quality discipline

The output quality of a loop is set by the system around it, not the loop itself:

- Keep the codebase clean; loops amplify whatever conventions exist.
- Give every loop a way to verify its own work (skills with quantitative checks).
- Use a second agent with fresh context for review; the builder is a biased judge of its own output.
- When a cycle produces a bad result, fix the system prompt, skill, or criteria, not just the result, so every future cycle inherits the fix.

## Summary

| Loop | You hand off | Use when | Reach for |
|---|---|---|---|
| Turn-based | the check | exploring or deciding | verification skills |
| Goal-based | the stop condition | done is verifiable | `/goal` |
| Time-based | the trigger | work arrives on a schedule or from outside | `/loop`, `/schedule` |
| Proactive | the prompt | recurring, well-defined streams | all of the above, plus workflows |
