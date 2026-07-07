# Contributing

Improvements welcome. Ground rules:

1. **Procedures must be executable.** Every rule in the operating manual needs the three-part shape: procedure, one short example of it working, the failure it prevents. "Be careful" is not a procedure.
2. **Loop guidance follows the primitives.** Suggestions map to real Claude Code features (`/goal`, `/loop`, `/schedule`, workflows, skills). No hypothetical commands.
3. **Suggest, never install.** Nothing in this skill may create automation without an explicit user yes. Changes that weaken that rule will be declined.
4. **Validate before opening a PR:** `python3 scripts/validate.py` must pass (CI runs the same check).
5. Keep SKILL.md under 500 lines; put depth in `references/`.
