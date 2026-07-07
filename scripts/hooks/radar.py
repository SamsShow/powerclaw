#!/usr/bin/env python3
"""powerclaw radar: detect repeated request shapes and surface a loop-suggestion cue.

UserPromptSubmit hook. Logs a token signature of each prompt per project and,
when the current prompt closely matches 2+ prompts from the last 7 days,
injects a context cue telling Claude to suggest the matching loop primitive.
Disable with POWERCLAW=off or POWERCLAW_RADAR=off.
"""
import json, os, re, sys, time, hashlib
from pathlib import Path

if "off" in (os.environ.get("POWERCLAW", "").lower(), os.environ.get("POWERCLAW_RADAR", "").lower()):
    sys.exit(0)

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

prompt = (data.get("prompt") or "").strip()
if len(prompt) < 12 or prompt.startswith("/"):
    sys.exit(0)

STOP = set(
    "a an the and or but if then else for to of in on at by with from is are was were be been "
    "being do does did done can could will would should may might must i you we they he she it "
    "this that these those my your our their me us them what which who how when where why not "
    "no yes please help make get let also just now new use using".split()
)
tokens = frozenset(t for t in re.findall(r"[a-z0-9]+", prompt.lower()) if t not in STOP and len(t) > 2)
if len(tokens) < 4:
    sys.exit(0)

state = Path.home() / ".powerclaw"
state.mkdir(exist_ok=True)
key = hashlib.sha256((data.get("cwd") or os.getcwd()).encode()).hexdigest()[:16]
log = state / f"radar-{key}.jsonl"

now = time.time()
entries = []
if log.exists():
    for line in log.read_text(errors="ignore").splitlines()[-200:]:
        try:
            e = json.loads(line)
            if now - e["ts"] < 7 * 86400:
                entries.append(e)
        except Exception:
            pass

def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 0.0

matches = [e for e in entries if jaccard(tokens, e["tokens"]) >= 0.5]

entries.append({"ts": now, "tokens": sorted(tokens)})
log.write_text("\n".join(json.dumps(e) for e in entries[-200:]) + "\n")

if len(matches) >= 2:
    sig = hashlib.sha256(" ".join(sorted(tokens)).encode()).hexdigest()[:12]
    cooldown = state / f"radar-cool-{key}-{sig}"
    if cooldown.exists() and now - cooldown.stat().st_mtime < 86400:
        sys.exit(0)
    cooldown.touch()
    print(
        "<powerclaw-radar>This request closely resembles "
        f"{len(matches)} earlier requests in this project from the last 7 days. "
        "After finishing the task, suggest the matching automation once: /goal if done-criteria are "
        "deterministic, /loop if it polls an external system, /schedule if it is time-driven, or a "
        "skill if it is a repeatable procedure. Include a ready-to-paste command, the stop condition, "
        "and rough cost. Never create automation without an explicit yes; if the user already declined "
        "this suggestion, do not repeat it.</powerclaw-radar>"
    )
sys.exit(0)
