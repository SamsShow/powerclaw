#!/usr/bin/env python3
"""powerclaw risk gate: irreversible-class commands must state their verification, once.

PreToolUse hook (Bash). Denies the first attempt at an irreversible-class command
with instructions to state (1) how the target was verified and (2) the rollback,
then allows the identical retry. Disable with POWERCLAW=off or POWERCLAW_RISK=off.
"""
import json, os, re, sys, hashlib, time
from pathlib import Path

if "off" in (os.environ.get("POWERCLAW", "").lower(), os.environ.get("POWERCLAW_RISK", "").lower()):
    sys.exit(0)

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if data.get("tool_name") != "Bash":
    sys.exit(0)
cmd = (data.get("tool_input") or {}).get("command", "")

PATTERNS = [
    (r"\brm\s+(-[a-z]*r[a-z]*f|-[a-z]*f[a-z]*r)[a-z]*\b", "recursive force delete"),
    (r"\bgit\s+push\b[^\n]*(--force\b|\s-f\b)", "force push"),
    (r"\bgit\s+reset\s+--hard\b", "hard reset"),
    (r"\bgit\s+clean\s+-[a-z]*f", "git clean"),
    (r"\bdrop\s+(table|database|schema)\b", "SQL drop"),
    (r"\btruncate\s+table\b", "SQL truncate"),
    (r"\bchmod\s+-R\s+777\b", "world-writable recursive chmod"),
    (r"\bmkfs\b|\bdd\s[^\n]*of=/dev/", "disk-level write"),
    (r"(curl|wget)[^|;\n]*\|\s*(ba|z)?sh\b", "pipe remote script to a shell"),
]
hit = next((label for pat, label in PATTERNS if re.search(pat, cmd, re.I)), None)
if not hit:
    sys.exit(0)

# temp and scratchpad deletes are routine, not irreversible-class
if hit == "recursive force delete" and re.search(r"rm\s+-\S+\s+((/private)?/tmp/|\S*scratchpad)", cmd, re.I):
    sys.exit(0)

state = Path.home() / ".powerclaw"
state.mkdir(exist_ok=True)
marker = state / f"risk-{hashlib.sha256(cmd.encode()).hexdigest()[:16]}"
if marker.exists() and time.time() - marker.stat().st_mtime < 3600:
    marker.unlink(missing_ok=True)
    sys.exit(0)
marker.touch()

reason = (
    f"powerclaw risk gate: this is an irreversible-class command ({hit}). Before retrying, state in "
    "your reply: (1) how you verified the target is correct, re-derived rather than assumed (paths "
    "listed, branch confirmed, counts checked), and (2) the rollback if it is wrong. Then retry the "
    "identical command and it will pass. Prefer a reversible alternative (move to a backup dir, a new "
    "branch) where one exists. Set POWERCLAW_RISK=off to disable."
)
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": reason,
}}))
sys.exit(0)
