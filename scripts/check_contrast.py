#!/usr/bin/env python3
"""Check the colour pairs in scripts/contrast_pairs.json against tokens/tokens.json (WCAG 2 contrast ratio)."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
tok = json.loads((ROOT / "tokens" / "tokens.json").read_text())
by = {t["name"]: t["value"] for t in tok["color"]["tokens"]}
by["white-on-error-large"] = "#ffffff"          # white text on error is allowed for large text only
def resolve(v):
    m = re.match(r"^\{(.+)\}$", v)
    return resolve(by[m.group(1)]) if m else v
def lum(h):
    h = h.lstrip("#"); r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
PAIRS = json.loads((ROOT / "scripts" / "contrast_pairs.json").read_text())["pairs"]

# Grounds that carry no text, so they need no pair. Each needs a reason.
EXEMPT = {
    "surface-card-soft": "translucent decoration behind a diagram lane; never carries text",
    "line": "rule colour, not a ground", "line-soft": "rule colour, not a ground",
    "navy-line": "rule colour, not a ground", "attention-line": "rule colour, not a ground",
    "chart-light": "chart segment fill, labelled directly",
}

def coverage():
    """Every ground a token names must be tested against the text that sits on it."""
    grounds = [t["name"] for t in tok["color"]["tokens"]
               if (t["name"].startswith(("bg-", "surface-", "attention-bg", "positive-bg"))
                   or t["name"] in ("navy", "success", "error", "warning", "info"))
               and not ALIAS_ONLY(t) and t["name"] not in EXEMPT]
    stale = [k for k in EXEMPT if k not in by]
    if stale:
        print("EXEMPT names a token that no longer exists: " + ", ".join(stale)); sys.exit(1)
    tested = {bg for _, bg, _ in PAIRS}
    missing = [g for g in grounds if g not in tested]
    for g in grounds:
        print(f"{'ok  ' if g in tested else 'MISS'} ground {g}")
    if missing:
        print(f"\n{len(missing)} ground(s) with no contrast pair: {', '.join(missing)}"
              "\nAdd one to scripts/contrast_pairs.json, or list it in EXEMPT with a reason.")
        sys.exit(1)
    print(f"\nAll {len(grounds)} grounds are covered")

def ALIAS_ONLY(t):
    return bool(re.match(r"^\{(.+)\}$", t["value"]))

if "--coverage" in sys.argv:
    coverage(); sys.exit(0)

fails = 0
for fg, bg, need in PAIRS:
    r = ratio(resolve(by[fg]), resolve(by[bg]))
    ok = r >= need
    if not ok: fails += 1
    print(f"{'ok  ' if ok else 'FAIL'} {fg} on {bg}: {r:.1f}:1 (need {need}:1)")
if fails:
    print(f"\n{fails} pair(s) below the minimum"); sys.exit(1)
print("\nAll contrast pairs pass")
