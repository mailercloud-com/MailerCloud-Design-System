#!/usr/bin/env python3
"""Check that consumers use tokens instead of restating their values.

  python scripts/check_usage.py

Scans the files that build documents -- component previews and the deck kit --
and fails when one of them writes a design value as a literal:

  * a colour that is not a token value (and never pure black or white);
  * a var(--name) that no token defines;
  * a font size, radius or spacing step that is not on the scale.

A line that must contain a literal (the deck kit's own lint, for instance)
carries a `check-usage: allow` comment saying why.

Generated files (dist/, index.html) are excluded: they are output, not source.
Geometry -- width, height, left, top, and the padding that positions content
inside a fixed-size diagram node -- is layout, not spacing, and is not checked.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOK = json.loads((ROOT / "tokens" / "tokens.json").read_text())
ALIAS = re.compile(r"^\{(.+)\}$")

COLOR = {t["name"]: t["value"] for t in TOK["color"]["tokens"]}
def resolve(v):
    m = ALIAS.match(v)
    return resolve(COLOR[m.group(1)]) if m else v

COLOR_VALUES = {resolve(v).lower() for v in COLOR.values()}
NAMES = set(COLOR) | {t["name"] for fam in ("spacing", "radius", "shadow") for t in TOK[fam]["tokens"]}
NAMES |= {f"font-{k}" for k in TOK["type"]["families"]}
SPACE = {int(t["value"].removesuffix("px")) for t in TOK["spacing"]["tokens"]}
RADIUS = {t["value"] for t in TOK["radius"]["tokens"]}
SLIDE_SIZES = {int(s["fontSize"].removesuffix("px"))
               for g in TOK["type"]["groups"] for s in g["styles"] if s["fontSize"].endswith("px")}

TARGETS = sorted(ROOT.glob("components/*/preview.html")) + sorted(ROOT.glob("tools/**/*.py"))

def check(path):
    text = path.read_text()
    rel = path.relative_to(ROOT)
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if "check-usage: allow" in line or line.lstrip().startswith("#"):
            continue
        where = f"{rel}:{i}"
        for hexv in re.findall(r"#[0-9a-fA-F]{6}\b", line):
            if hexv.lower() in ("#000000", "#ffffff"):
                out.append(f"{where}: pure black or white; use ink or text-inverse")
            elif hexv.lower() not in COLOR_VALUES:
                out.append(f"{where}: {hexv} is not a token value; add it to tokens.json or use a token")
        for rgba in re.findall(r"rgba\([^)]*\)", line):
            if rgba.replace(" ", "") not in {v.replace(" ", "") for v in COLOR_VALUES} and \
               not any(rgba in resolve(t["value"]) for t in TOK["shadow"]["tokens"]):
                out.append(f"{where}: {rgba} is not a token value")
        for name in re.findall(r"var\(--([a-z0-9-]+)\)", line):
            if name not in NAMES:
                out.append(f"{where}: var(--{name}) names no token")
        for size in re.findall(r"font-size:\s*(\d+)px", line):
            if int(size) not in SLIDE_SIZES:
                out.append(f"{where}: font-size {size}px is not on the type scale "
                           f"({', '.join(str(s) for s in sorted(SLIDE_SIZES))})")
        for rad in re.findall(r"border-radius:\s*([0-9]+px)", line):
            if rad not in RADIUS:
                out.append(f"{where}: border-radius {rad} is not on the radius scale "
                           f"({', '.join(sorted(RADIUS))})")
        for gap in re.findall(r"gap:\s*(\d+)px", line):
            if int(gap) not in SPACE and int(gap) != 0:
                out.append(f"{where}: gap {gap}px is not on the spacing scale")
    return out

def main():
    problems = [p for t in TARGETS for p in check(t)]
    for p in problems:
        print("  -", p)
    if problems:
        print(f"\n{len(problems)} value(s) restated instead of referenced. "
              "Use a token, or add one to tokens/tokens.json with a usage note.")
        sys.exit(1)
    print(f"{len(TARGETS)} consumer file(s) use tokens only")

if __name__ == "__main__":
    main()
