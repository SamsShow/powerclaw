# powerclaw

**Frontier discipline on any model. Loop suggestions when work repeats. Enforced by hooks, not vibes.**

An open-source [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) for Claude. Models get deprecated and repriced; procedures do not. The quality gap between a frontier model and the tier below it is mostly a set of habits, and habits can be written down and run anywhere. powerclaw does two things:

1. **The operating manual.** Eight procedures that raise output quality on any Claude model: read the real request beneath the words, decompose into independently checkable pieces, spend effort where the risk lives, verify claims by re-deriving them, label known versus guessed out loud, attack your own conclusion before shipping, lead with the answer, and catch the mistakes that look like competence. Every answer passes a five-question self-test before it ships.
2. **The loop radar.** While working, Claude watches for automation signals: a request repeating, a task with deterministic done-criteria, work blocked on CI or code review, cadence words like "every morning", the same operation over many items. When one fires, it suggests the matching Claude Code primitive (`/goal`, `/loop`, `/schedule`, a workflow, or a verification skill) with a ready-to-paste command, the stop condition, and the cost. It suggests once, and it never creates automation without an explicit yes.

## Try the difference

Give a model this rigged question with and without powerclaw:

> A report says revenue grew from $4.0M to $4.2M and calls it a 20% gain. Ship it?

Without discipline, the sentence reads smoothly and gets waved through. With the manual loaded, the claim gets re-derived: 0.2 / 4.0 is 5%, not 20%, and the answer refuses to ship it. Verification by re-derivation is procedure 4; the self-test makes it non-optional.

## Install

### Claude Code (under 2 minutes)

```bash
git clone https://github.com/SamsShow/powerclaw.git ~/.claude/skills/powerclaw
```

Or as a plugin:

```
/plugin marketplace add SamsShow/powerclaw
/plugin install powerclaw@powerclaw
```

Or with the skills CLI:

```bash
npx skills add SamsShow/powerclaw
```

### Always-on mode (Claude Code)

By default a skill fires when its description matches the task. Always-on mode injects the pre-send gate and loop radar into every session via a SessionStart hook, so the discipline applies even when the skill is never explicitly triggered.

Plugin installs get this automatically (`hooks/hooks.json` ships with the plugin). For a clone or symlink install, add this to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "bash ~/.claude/skills/powerclaw/scripts/radar-context.sh" } ] }
    ]
  }
}
```

The injected block is about 20 lines, a deliberate summary; Claude loads the full skill when the work calls for it.

### Enforcement layer (Claude Code)

Context blocks advise; hooks enforce. Version 2.0.0 adds three hooks that make the discipline mechanical. Plugin installs get all of them automatically. For a clone or symlink install, register them the same way as the SessionStart hook above:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "python3 ~/.claude/skills/powerclaw/scripts/hooks/radar.py" } ] }
    ],
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "python3 ~/.claude/skills/powerclaw/scripts/hooks/risk-gate.py" } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "python3 ~/.claude/skills/powerclaw/scripts/hooks/stop-gate.py" } ] }
    ]
  }
}
```

What each one does:

- **Radar** fingerprints every prompt (token signature, per project) and compares it against the last 7 days. When a request shape recurs 2+ times, it injects a cue to suggest the matching loop primitive after the task finishes. The detection is mechanical, so it works even when the repeats are days apart and the model would never connect them. One cue per shape per day.
- **Risk gate** intercepts irreversible-class Bash commands: recursive force deletes, force pushes, hard resets, SQL drops and truncates, disk-level writes, piping remote scripts to a shell. The first attempt is denied with instructions to state how the target was verified and what the rollback is; the identical retry within the hour passes. Temp-directory and scratchpad deletes are exempt. This is procedure 3 (effort follows risk) and procedure 4 (verify by re-deriving) as a mechanism instead of a request.
- **Stop gate** holds a substantive final answer once per session until the five-question self-test has been run. It respects the stop-hook-active flag, so it can never loop.

Kill switches, as environment variables: `POWERCLAW=off` disables everything; `POWERCLAW_RADAR=off`, `POWERCLAW_RISK=off`, `POWERCLAW_GATE=off` disable one each. State lives in `~/.powerclaw/` and prunes itself. All hooks are dependency-free Python 3 (stdlib only) and fail open: a parse error or missing file exits silently rather than blocking work.

### claude.ai (paid plans)

1. Download `powerclaw.zip` from the [latest release](https://github.com/SamsShow/powerclaw/releases/latest) (or run `scripts/package-zip.sh`).
2. Settings, Capabilities, enable Skills, upload the zip.

### API

Upload the same zip via the [Skills API](https://docs.claude.com/en/api/skills), then reference the skill in your requests.

## What's inside

```
SKILL.md                          The pre-send gate, the loop radar, six non-negotiables
references/operating-manual.md    Eight procedures: each with the move, an example, the failure prevented
references/loop-playbook.md       Four loop types, exact commands, suggestion etiquette, token discipline
scripts/validate.py               CI check: strict frontmatter, cross-references
scripts/package-zip.sh            Builds the claude.ai upload zip
scripts/radar-context.sh          SessionStart hook payload for always-on mode
hooks/hooks.json                  Auto-registers all hooks for plugin installs
scripts/hooks/radar.py            Repeated-request detection, injects loop-suggestion cues
scripts/hooks/risk-gate.py        Irreversible commands must state verification and rollback
scripts/hooks/stop-gate.py        Holds substantive answers for the self-test, once per session
```

## Companions

- [formulary](https://github.com/SamsShow/formulary-claude): which model, which parameters, which tested snippet. powerclaw governs how the work is done once those are set.
- [deckle-paper](https://github.com/SamsShow/deckle-paper): design direction and taste for UI work.

## Credits

The loop taxonomy follows the Claude Code team's guidance on designing loops (turn-based, goal-based, time-based, proactive), written by [@delba_oliveira](https://x.com/delba_oliveira). The operating-manual framing (portable procedures over rented models) is the honest core of the "extract the manual" idea circulating during the Fable 5 pricing change.

## License

MIT
