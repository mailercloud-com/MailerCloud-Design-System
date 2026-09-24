#!/usr/bin/env python3
"""Build the generated files from tokens/tokens.json.

  python scripts/build_tokens.py          write dist/tokens.css, dist/tokens.dtcg.json and index.html
  python scripts/build_tokens.py --check  fail if the generated files are out of date (used in CI)

tokens/tokens.json is the single source of truth. Never edit the generated files by hand.
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOK = json.loads((ROOT / "tokens" / "tokens.json").read_text())
ALIAS = re.compile(r"^\{([A-Za-z0-9][A-Za-z0-9_.-]*)\}$")

def color_value(v):
    m = ALIAS.match(v)
    return f"var(--{m.group(1)})" if m else v

def resolve(name, by):
    v = by[name]["value"]
    m = ALIAS.match(v)
    return resolve(m.group(1), by) if m else v

def css():
    o = [f"/* Generated from tokens/tokens.json (version {TOK['version']}). Do not edit. */", ":root {"]
    o.append("  /* color */")
    for t in TOK["color"]["tokens"]: o.append(f"  --{t['name']}: {color_value(t['value'])};")
    for fam, title in (("spacing", "spacing"), ("radius", "radius"), ("shadow", "shadow")):
        o.append(f"  /* {title} */")
        for t in TOK[fam]["tokens"]: o.append(f"  --{t['name']}: {t['value']};")
    o.append("  /* font families */")
    for k, v in TOK["type"]["families"].items(): o.append(f"  --font-{k}: {v};")
    o.append("}")
    for g in TOK["type"]["groups"]:
        for st in g["styles"]:
            fam = st.get("family") or g["family"]
            o.append(f".{st['name']} {{ font-family: var(--font-{fam}); font-size: {st['fontSize']}; line-height: {st['lineHeight']}; font-weight: {st['fontWeight']}; }}")
    return "\n".join(o) + "\n"

def parse_shadow(v):
    m = re.match(r"^(-?\d+)px\s+(-?\d+)px\s+(\d+)(?:px)?\s+(.+)$", v)
    if not m: return v
    return {"color": m.group(4), "offsetX": m.group(1) + "px", "offsetY": m.group(2) + "px", "blur": m.group(3) + "px", "spread": "0px"}

def dtcg():
    d = {"$description": f"MailerCloud Design System {TOK['version']}", "color": {}, "spacing": {}, "radius": {}, "shadow": {}, "font": {}}
    for t in TOK["color"]["tokens"]:
        m = ALIAS.match(t["value"])
        d["color"][t["name"]] = {"$type": "color", "$value": "{color.%s}" % m.group(1) if m else t["value"], "$description": t["usage"]}
    for fam, typ in (("spacing", "dimension"), ("radius", "dimension")):
        for t in TOK[fam]["tokens"]: d[fam][t["name"]] = {"$type": typ, "$value": t["value"], "$description": t["usage"]}
    for t in TOK["shadow"]["tokens"]: d["shadow"][t["name"]] = {"$type": "shadow", "$value": parse_shadow(t["value"]), "$description": t["usage"]}
    for k, v in TOK["type"]["families"].items():
        d["font"][k] = {"$type": "fontFamily", "$value": [x.strip().strip('"') for x in v.split(",")]}
    return json.dumps(d, indent=2, ensure_ascii=False) + "\n"

def site():
    by = {t["name"]: t for t in TOK["color"]["tokens"]}
    def tier(n):
        if n.startswith(("text-", "surface-page", "surface-raised", "surface-inverse", "border-", "action-", "focus-", "status-")): return "Semantic"
        if n.startswith(("card-", "table-", "node-")): return "Component"
        if n.startswith("chart-") and n not in ("chart-grey", "chart-light"): return "Data visualisation"
        return "Primitive"
    groups = {}
    for t in TOK["color"]["tokens"]: groups.setdefault(tier(t["name"]), []).append(t)
    sw = []
    for g in ("Primitive", "Semantic", "Component", "Data visualisation"):
        cells = []
        for t in groups.get(g, []):
            hexv = resolve(t["name"], by); al = ALIAS.match(t["value"])
            cells.append(f'<div class="sw"><div class="chip" style="background:{hexv}"></div><b>{html.escape(t["name"])}</b><span>{hexv}{" → " + al.group(1) if al else ""}</span><i>{html.escape(t["usage"])}</i></div>')
        sw.append(f"<h3>{g}</h3><div class=\"swgrid\">{''.join(cells)}</div>")
    sp = "".join(f'<div class="row"><b>{t["name"]}</b><span>{t["value"]}</span><div class="bar" style="width:{t["value"]}"></div></div>' for t in TOK["spacing"]["tokens"])
    rd = "".join(f'<div class="rd" style="border-radius:{t["value"]}"><b>{t["name"]}</b><span>{t["value"]}</span></div>' for t in TOK["radius"]["tokens"])
    sh = "".join(f'<div class="shd" style="box-shadow:{t["value"]}"><b>{t["name"]}</b></div>' for t in TOK["shadow"]["tokens"])
    ty = "".join(f'<div class="ty"><span class="{s["name"]}">{html.escape(s.get("sample", s["name"]))}</span><small>{s["name"]} · {s["fontSize"]} · {s["fontWeight"]}</small></div>' for g in TOK["type"]["groups"] for s in g["styles"])
    comps = []
    for p in sorted((ROOT / "components").glob("*/preview.html")):
        first = p.read_text().split("\n", 1)[0]
        m = re.search(r"height=(\d+)", first); h = int(m.group(1)) if m else 300
        name = p.parent.name
        comps.append(f'<div class="comp"><h3>{name}</h3><iframe src="components/{name}/preview.html" style="height:{h + 30}px" title="{name}"></iframe></div>')
    docs = "".join(f'<li><a href="{p.as_posix()}">{p.stem}</a></li>' for p in sorted(x.relative_to(ROOT) for x in (ROOT / "docs").rglob("*.md")))
    return f"""<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>MailerCloud Design System {TOK['version']}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="dist/tokens.css">
<style>
body{{margin:0;font-family:var(--font-sans);color:var(--text-primary);background:var(--surface-page);line-height:1.5}}
main{{max-width:1180px;margin:0 auto;padding:48px 32px 96px}} h1{{font-size:44px;margin:0 0 8px}} h2{{font-size:28px;margin:64px 0 16px;border-top:4px solid var(--ink);padding-top:16px}} h3{{font-size:18px;margin:32px 0 12px}}
.lead{{font-size:18px;color:var(--text-secondary);max-width:760px}} .swgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px}}
.sw{{display:flex;flex-direction:column;gap:2px;font-size:13px}} .sw .chip{{height:56px;border-radius:12px;border:1px solid var(--border-subtle);margin-bottom:6px}} .sw span{{color:var(--text-secondary)}} .sw i{{font-style:normal;color:var(--text-secondary);font-size:12px}}
.row{{display:flex;align-items:center;gap:16px;margin:6px 0;font-size:14px}} .row b{{width:180px}} .row span{{width:70px;color:var(--text-secondary)}} .bar{{height:14px;background:var(--brand-blue);border-radius:4px}}
.rd{{display:inline-flex;flex-direction:column;gap:4px;width:150px;height:90px;margin:0 16px 16px 0;background:var(--bg-sky);align-items:center;justify-content:center;font-size:13px}}
.shd{{display:inline-flex;width:170px;height:90px;margin:0 24px 24px 0;background:var(--surface-raised);border-radius:var(--radius-card);align-items:center;justify-content:center;font-size:13px}}
.ty{{margin:12px 0;display:flex;flex-direction:column}} .ty small{{color:var(--text-secondary)}}
.comp iframe{{width:100%;border:1px solid var(--border-subtle);border-radius:12px;background:#fff}} a{{color:var(--text-link);text-decoration:underline}}
</style></head><body><main>
<h1>MailerCloud Design System</h1>
<p class="lead">Version {TOK['version']}. Generated from <code>tokens/tokens.json</code> by <code>scripts/build_tokens.py</code>. Brand rules, accessibility, data visualisation and governance are in <code>docs/</code>.</p>
<h2>Colour</h2>{''.join(sw)}
<h2>Type</h2>{ty}
<h2>Spacing</h2>{sp}
<h2>Radius</h2>{rd}
<h2>Shadow</h2>{sh}
<h2>Components</h2>{''.join(comps)}
<h2>Documentation</h2><ul>{docs}</ul>
</main></body></html>
"""

def main():
    out = {ROOT / "dist" / "tokens.css": css(), ROOT / "dist" / "tokens.dtcg.json": dtcg(), ROOT / "index.html": site()}
    if "--check" in sys.argv:
        bad = [str(p.relative_to(ROOT)) for p, c in out.items() if not p.exists() or p.read_text() != c]
        if bad:
            print("Out of date: " + ", ".join(bad) + "\nRun: python scripts/build_tokens.py"); sys.exit(1)
        print("Generated files are up to date"); return
    for p, c in out.items(): p.write_text(c); print("wrote", p.relative_to(ROOT))

if __name__ == "__main__": main()
