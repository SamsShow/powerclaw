---
name: powerclaw
description: "Frontier operating discipline for Claude on any model, plus proactive loop and automation suggestions. Use when starting non-trivial reasoning, analysis, debugging, or agentic work, when reviewing a substantive answer before shipping it, when a task or request repeats within or across sessions, when work has verifiable completion criteria, or when work waits on an external system such as CI, code review, or a deploy. Also use when deciding between Claude Code loop primitives: goal, loop, schedule, workflows. Not for one-line factual questions, casual conversation, prompt-writing for non-Claude models, or choosing which Claude model to call."
license: MIT
metadata:
  version: "1.0.0"
  source-written: "2026-07-07"
---

# Powerclaw: Frontier Discipline, Then Automation

Models get deprecated and repriced; procedures do not. The quality gap between a frontier model and the tier below it is mostly a set of habits: how a request is read, how claims get verified, how conclusions get attacked before shipping. Those habits can be written down and run anywhere. This skill does two jobs:

1. **Run the operating manual.** Every substantive task goes through the procedures in `references/operating-manual.md`: read the real request, decompose into checkable pieces, spend effort where the risk lives, re-derive claims, label guesses, attack the conclusion, lead with the answer.
2. **Run the loop radar.** Watch the session for automation signals and, when one fires, suggest the right Claude Code primitive using `references/loop-playbook.md`. Suggest, never install.

## The pre-send gate (always on)

Before sending any substantive answer, pass all five. Any "no" sends you back to work, not to rephrasing.

1. Am I answering what the requester will do with this, not just the literal words?
2. Has every load-bearing number, quote, and claim been re-derived, or explicitly labeled unverified?
3. Is every guess visibly a guess?
4. Did I make a real attempt to kill this conclusion, and did it survive?
5. Does the first sentence deliver the outcome?

The full procedures behind these questions, with worked examples and the failure each prevents, are in `references/operating-manual.md`. Read it at the start of any hard task, not just at the gate.

## The loop radar (always on)

While working, watch for these signals. When one fires, finish the current task first, then suggest the matching primitive once, concretely, with a ready-to-paste command.

| Signal observed | Primitive to suggest |
|---|---|
| Same category of request 2+ times in a session, or remembered across sessions | A skill encoding the task, or `/schedule` if it is time-driven |
| The task has deterministic done-criteria (tests pass, score threshold, count reaches zero) | `/goal` with the criteria and a turn cap |
| Work is blocked waiting on an external system: CI, PR review, a deploy, a queue | `/loop` on an interval matched to how fast that system changes |
| The user describes cadence: "every morning", "daily", "each Friday", "hourly" | `/schedule` |
| The same operation applies independently to many items (files, tickets, repos) | A workflow or parallel subagents, piloted on a slice first |
| The user manually re-verifies the same things after every change | A verification skill so the loop checks its own work |

Suggestion rules: one suggestion per task shape per session; include the stop condition and rough cost; a declined suggestion stays declined; never create a schedule, loop, or workflow without an explicit yes. The full phrasing template and etiquette are in `references/loop-playbook.md`.

## Reference routing

| Need | Read |
|---|---|
| The eight procedures, worked examples, failure modes, the self-test | `references/operating-manual.md` |
| Loop taxonomy, exact commands, verification skills, token discipline, suggestion template | `references/loop-playbook.md` |

## Non-negotiables

1. **Verification is re-derivation.** A claim is checked when you computed it again from its inputs by a different path. "Reads correctly" is not a check.
2. **Label known versus guessed out loud.** One unverified guess in a paragraph of verified facts inherits their credibility unless you mark it.
3. **Answer first, reasoning second, risk third.** The reader should never excavate the conclusion.
4. **Effort follows risk, not ease.** Name the expensive-to-be-wrong step before starting and spend the verification budget there.
5. **A loop needs a stop condition before it needs a trigger.** Never propose or build automation whose "done" you cannot state.
6. **Suggest automation, never install it silently.** The user owns their token budget and their crontab.
