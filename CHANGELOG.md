# Changelog

## 2.0.0 (2026-07-07)

- Enforcement layer: the discipline is now mechanized, not just described.
- Radar hook (UserPromptSubmit): detects repeated request shapes per project (token-signature similarity over a 7-day window) and injects a loop-suggestion cue. Daily cooldown per shape.
- Risk gate (PreToolUse): irreversible-class Bash commands are denied once with instructions to state the verification and rollback; the identical retry passes. Temp and scratchpad deletes are exempt.
- Stop gate (Stop): once per session, a substantive final answer is held until the five-question self-test runs. Respects stop_hook_active, so it can never loop.
- Kill switches: POWERCLAW=off for everything, POWERCLAW_RADAR / POWERCLAW_RISK / POWERCLAW_GATE per hook. All hooks are stdlib Python, no dependencies.

## 1.1.0 (2026-07-07)

- Always-on mode: a SessionStart hook (`scripts/radar-context.sh`) injects the pre-send gate and loop radar into every session's context.
- Plugin installs pick the hook up automatically via `hooks/hooks.json`; manual installs register it in `~/.claude/settings.json` (see README).

## 1.0.0 (2026-07-07)

- Initial release.
- The operating manual: eight procedures with worked examples and the failure each prevents.
- The pre-send self-test: five questions gating every substantive answer.
- The loop radar: six detection signals mapped to Claude Code primitives.
- The loop playbook: turn-based, goal-based, time-based, and proactive loops, with suggestion etiquette and token discipline.
