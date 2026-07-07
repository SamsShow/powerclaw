# Changelog

## 1.1.0 (2026-07-07)

- Always-on mode: a SessionStart hook (`scripts/radar-context.sh`) injects the pre-send gate and loop radar into every session's context.
- Plugin installs pick the hook up automatically via `hooks/hooks.json`; manual installs register it in `~/.claude/settings.json` (see README).

## 1.0.0 (2026-07-07)

- Initial release.
- The operating manual: eight procedures with worked examples and the failure each prevents.
- The pre-send self-test: five questions gating every substantive answer.
- The loop radar: six detection signals mapped to Claude Code primitives.
- The loop playbook: turn-based, goal-based, time-based, and proactive loops, with suggestion etiquette and token discipline.
