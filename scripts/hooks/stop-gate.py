#!/usr/bin/env python3
"""powerclaw stop gate: one forced pass of the pre-send self-test per session.

Stop hook. When the turn's final answer is substantive (over ~900 chars) and the
session has not been gated yet, blocks the stop once and instructs Claude to run
the five-question self-test before shipping. Respects stop_hook_active so it can
never loop. Disable with POWERCLAW=off or POWERCLAW_GATE=off.
"""
import json, os, sys, time
from pathlib import Path

if "off" in (os.environ.get("POWERCLAW", "").lower(), os.environ.get("POWERCLAW_GATE", "").lower()):
    sys.exit(0)

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if data.get("stop_hook_active"):
    sys.exit(0)

state = Path.home() / ".powerclaw"
state.mkdir(exist_ok=True)
now = time.time()
for old in state.glob("gate-*"):
    if now - old.stat().st_mtime > 7 * 86400:
        old.unlink(missing_ok=True)

marker = state / f"gate-{data.get('session_id', 'unknown')}"
if marker.exists():
    sys.exit(0)

last = ""
tp = data.get("transcript_path")
if tp and Path(tp).exists():
    for line in Path(tp).read_text(errors="ignore").splitlines()[::-1]:
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("type") == "assistant":
            for block in (e.get("message") or {}).get("content", []):
                if isinstance(block, dict) and block.get("type") == "text":
                    last = block.get("text", "") or last
            if last:
                break
if len(last) < 900:
    sys.exit(0)

marker.touch()
print(json.dumps({"decision": "block", "reason": (
    "powerclaw pre-send gate (fires once per session): before this answer ships, run the "
    "five-question self-test: (1) does it answer what the requester will do with it, not just the "
    "literal words; (2) is every load-bearing number, quote, and claim re-derived or explicitly "
    "labeled unverified; (3) is every guess visibly a guess; (4) did you make a real attempt to kill "
    "the conclusion, and did it survive; (5) does the first sentence deliver the outcome. If all five "
    "pass, restate the final answer unchanged and stop. If any fail, fix that first. "
    "Set POWERCLAW_GATE=off to disable."
)}))
sys.exit(0)
