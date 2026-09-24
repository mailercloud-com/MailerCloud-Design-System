#!/usr/bin/env python3
"""Client solution deck builder (MailerCloud design system).

Builds the slide files for a "move outbound email to MailerCloud" client deck
from one JSON config, using the MailerCloud design tokens. Output is a Slides
artifact folder: project/deck.json + project/slides/<id>.html.

  python build_deck.py config.example.json out_dir [--logo /_blob/<id>]

Then publish out_dir/project/deck.json plus the slides with the Artifact tool,
or hand the folder to Claude ("publish this deck").
"""
import argparse, html, json, math, os, re, sys

# ---------------------------------------------------------------- tokens ----
INK = "#020a13"; MUTED = "#22364c"; NAVY = "#091929"; BLUE = "#046dff"; CARD = "#fdfdf8"
SKY = "#5bbdee"; LIME = "#dfec54"; MINT = "#82d5c5"; GREEN = "#8cd480"
PINK = "#fbd3eb"; CREAM = "#fbf9ae"; PAPER = "#f8fdf7"
ZEBRA_LIME = "#f4f6d6"; ZEBRA_CREAM = "#f1efb4"; POSITIVE_BG = "#b7f0cf"; POSITIVE_INK = "#0c4a2e"
NAVY_LINE = "#2b3a63"; CODE_KEY = "#8fb4ff"; CODE_STR = "#8be3a0"; CODE_TXT = "#cbd5e1"; LIGHT_ON_NAVY = "#c7d7ec"
SH = "10px 10px 0 rgba(2,10,19,0.18)"; SH_DARK = "10px 10px 0 rgba(2,10,19,0.28)"; SH_SM = "8px 8px 0 rgba(2,10,19,0.22)"
FONT = "'Poppins', Arial, sans-serif"; MONO = "'JetBrains Mono', 'Courier New', monospace"

def eb(c): return f"{c['client']} · {c['_section']}" if c.get("_section") else None

def esc(s): return html.escape(str(s), quote=False)
def n(x): return f"{int(x):,}"
def k(x): return f"{int(x)//1000}K"

# ------------------------------------------------------------ components ----
def pill(text, bg, fg=INK, size=24, weight=600, pad="6px 20px", flow=True):
    al = "align-self:flex-start; " if flow else ""
    return (f'<p style="{al}background:{bg}; color:{fg}; font-size:{size}px; font-weight:{weight}; '
            f'line-height:1.3; padding:{pad}; border-radius:30px">{esc(text)}</p>')

def card(inner, dark=False, pad=32, gap=12, flex=True, extra=""):
    bg = NAVY if dark else CARD
    fg = f"color:{CARD}; " if dark else ""
    sh = SH_DARK if dark else SH
    f = "flex:1; " if flex else ""
    return (f'<div style="{f}display:flex; flex-direction:column; gap:{gap}px; background:{bg}; {fg}'
            f'padding:{pad}px; border-radius:28px; box-shadow:{sh}{extra}">{inner}</div>')

def h3(text, size=40, color=None):
    c = f"; color:{color}" if color else ""
    return f'<h3 style="font-size:{size}px; font-weight:700; line-height:1.2{c}">{esc(text)}</h3>'

def ptext(text, size=32, lh=1.4, color=None, weight=None, extra=""):
    c = f"; color:{color}" if color else ""
    w = f"; font-weight:{weight}" if weight else ""
    return f'<p style="font-size:{size}px; line-height:{lh}{c}{w}{extra}">{esc(text)}</p>'

def title(text, sub=None, eyebrow=None):
    parts = []
    if eyebrow:
        parts.append(f'<p style="font-size:24px; font-weight:600; letter-spacing:2px; text-transform:uppercase; line-height:1.3; color:{MUTED}">{esc(eyebrow)}</p>')
    parts.append(f'<h2 style="font-size:64px; font-weight:700; line-height:1.1">{esc(text)}</h2>')
    if sub: parts.append(f'<p style="font-size:32px; line-height:1.4">{esc(sub)}</p>')
    return '<div style="display:flex; flex-direction:column; gap:8px">\n' + "\n".join(parts) + "\n</div>"

def ul(items, size=32, color=None, tag="ul"):
    c = f"; color:{color}" if color else ""
    lis = "\n".join(f"<li>{esc(i)}</li>" for i in items)
    return f'<{tag} style="font-size:{size}px; line-height:1.4{c}">\n{lis}\n</{tag}>'

def banner(text, dark=False):
    bg, fg = (NAVY, CARD) if dark else (CARD, INK)
    return (f'<p style="align-self:stretch; background:{bg}; color:{fg}; font-size:32px; font-weight:600; '
            f'line-height:1.4; padding:22px 36px; border-radius:24px; box-shadow:{SH_SM}">{esc(text)}</p>')

def row(inner, gap=32, extra=""):
    return f'<div style="display:flex; flex-direction:row; gap:{gap}px{extra}">\n{inner}\n</div>'

def fill(inner, gap=40):
    """The content group under a title, centred vertically between the title block and the footer safe line."""
    return f'<div style="flex:1; display:flex; flex-direction:column; justify-content:center; gap:{gap}px">\n{inner}\n</div>'

def col(inner):
    return f'<div style="flex:1; display:flex; flex-direction:column; gap:16px; border-top:4px solid {INK}; padding:24px 0px 0px 0px">\n{inner}\n</div>'

def hair(color="rgba(2,10,19,0.16)"): return f"2px solid {color}"

def open_rows(headers, widths, rows, size=28, callout=None):
    """Open list instead of a boxed table: labels, hairline rules, no fills."""
    hd = "".join(f'<p style="width:{w}%; font-size:24px; font-weight:600; letter-spacing:1px; text-transform:uppercase; color:{MUTED}">{esc(h)}</p>' for h, w in zip(headers, widths))
    out = [f'<div style="display:flex; flex-direction:row; gap:32px; padding:0px 0px 12px 0px; border-bottom:{hair(INK)}">{hd}</div>']
    for r in rows:
        cells = "".join(f'<p style="width:{w}%; font-size:{size}px; line-height:1.3{"; font-weight:700" if j == 0 else ""}">{esc(x)}</p>' for j, (x, w) in enumerate(zip(r, widths)))
        out.append(f'<div style="display:flex; flex-direction:row; gap:32px; padding:22px 0px; border-bottom:{hair()}">{cells}</div>')
    if callout:
        k1, k2 = callout
        out.append(f'<div style="display:flex; flex-direction:row; gap:32px; align-items:center; background:{POSITIVE_BG}; padding:22px 32px; border-radius:24px">'
                   f'<p style="font-size:{size}px; font-weight:700; color:{POSITIVE_INK}">{esc(k1)}</p><p style="font-size:{size}px; color:{POSITIVE_INK}">{esc(k2)}</p></div>')
    return '<div style="display:flex; flex-direction:column; gap:0px">\n' + "\n".join(out) + "\n</div>"

def chips(labels, bg, fg, arrow):
    parts = []
    for i, l in enumerate(labels):
        if i: parts.append(f'<x-shape kind="arrow-right" style="background:{arrow}; width:40px; height:24px"></x-shape>')
        parts.append(pill(l, bg, fg, 24, 600, "6px 16px", flow=False))
    return '<div style="display:flex; flex-direction:row; align-items:center; gap:12px">' + "".join(parts) + "</div>"

def table(headers, widths, rows, size, zebra, last_row_bg=None, pad="22px 20px"):
    th = "".join(f'<th style="width:{w}%; color:{CARD}; text-align:left; padding:{pad}">{esc(h)}</th>' for h, w in zip(headers, widths))
    out = [f'<table style="width:1664px; font-size:{size}px; color:{INK}">',
           f'<tr style="background:{NAVY}">{th}</tr>']
    for i, r in enumerate(rows):
        bg = CARD if i % 2 == 0 else zebra
        if last_row_bg and i == len(rows) - 1: bg = last_row_bg
        cells = "".join(f'<td style="padding:{pad}">{"<b>"+esc(c)+"</b>" if j == 0 else esc(c)}</td>' for j, c in enumerate(r))
        out.append(f'<tr style="background:{bg}">{cells}</tr>')
    out.append("</table>")
    return "\n".join(out)

def node(x, y, w, h, inner, dark=False, pad="", gap=14):
    bg, bd = (NAVY, NAVY) if dark else (CARD, INK)
    return (f'<div style="position:absolute; left:{x}px; top:{y}px; width:{w}px; height:{h}px; background:{bg}; '
            f'border:3px solid {bd}; border-radius:28px; box-shadow:{SH_SM}; display:flex; flex-direction:column; '
            f'gap:{gap}px; padding:{pad}">{inner}</div>')

def conn(x1, y1, x2, y2, color=INK, w=4, dashed=False):
    d = "; border-style:dashed" if dashed else ""
    return f'<x-connector x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="color:{color}; border-width:{w}px{d}"></x-connector>'

def pin_p(x, y, w, text, size=24, weight=500, align="center", color=None, lh=1.4):
    c = f"; color:{color}" if color else ""
    return (f'<p style="position:absolute; left:{x}px; top:{y}px; width:{w}px; font-size:{size}px; '
            f'font-weight:{weight}; line-height:{lh}; text-align:{align}{c}">{text}</p>')

def icon(name, x, y, s, color=INK):
    return f'<x-icon name="{name}" style="position:absolute; left:{x}px; top:{y}px; width:{s}px; height:{s}px; color:{color}"></x-icon>'

# ---------------------------------------------------------------- slides ----
def s_cover(c):
    d = (f'<div style="position:absolute; left:1240px; top:400px; width:560px; height:560px; background:{GREEN}; border-radius:280px"></div>\n'
         f'<div style="position:absolute; left:1500px; top:120px; width:260px; height:260px; background:{LIME}; border-radius:130px"></div>\n'
         f'<div style="position:absolute; left:1380px; top:580px; width:280px; height:280px; background:{CARD}; border-radius:140px; box-shadow:12px 12px 0 rgba(2,10,19,0.25)"></div>\n'
         f'{icon("PaperPlane", 1460, 660, 120, NAVY)}')
    l1, l2 = c["cover_title"]
    body = (d + "\n" + pill(f"Solution proposal for {c['client']}", NAVY, CARD, 28, 600, "12px 28px") +
            f'\n<h1 style="font-size:88px; font-weight:700; line-height:1.1; width:1200px">{esc(l1)}<br>{esc(l2)}</h1>\n' +
            ptext(f"Keep {c['inbound_system']} for inbound. Route every outbound reply through MailerCloud.", 32, extra="; width:1000px") + "\n" +
            ptext(f"{c['meeting']} · {c['date']}", 26, color=MUTED, weight=500))
    notes = (f"Open with the problem in one sentence: about {n(c['volume'])} {c['use_case_short']} a day are being blocked on {c['provider']}. "
             f"The proposal keeps {c['inbound_system']} where it works (inbound) and moves only the outbound route to MailerCloud.")
    return dict(bg=SKY, body=body, notes=notes, gap=40, justify="center", cover=True)

def s_exec(c):
    pl = c["provider_limits"]
    cols = [("01", "The problem", f"{c['provider']} limits each mailbox to {n(pl['recipients_per_day'])} recipients a day and {pl['messages_per_min']} a minute. {c['client']} sends about {n(c['volume'])} {c['use_case_short']} a day."),
            ("02", "The solution", f"Keep {c['inbound_system']} for inbound. Send every reply through MailerCloud, signed with {c['client']}'s own domain."),
            ("03", "The outcome", c["outcome_text"])]
    inner = row("\n".join(col(ptext(a, 26, color=MUTED, weight=600) + h3(b) + ptext(t, 32, 1.45)) for a, b, t in cols), gap=48) + "\n" + banner(f"The ask: {c['ask']}", dark=True)
    body = title(f"{n(c['volume'])} replies a day, without the blocks", eyebrow=eb(c)) + "\n" + fill(inner, 56)
    notes = "This slide is the whole story for a reader who only has one minute: the problem, the fix and what changes. Every later slide backs one of these three columns."
    return dict(bg=LIME, body=body, notes=notes, gap=32)

def s_situation(c):
    pl = c["provider_limits"]
    cols = []
    for sc in c["situation_cards"]:
        if sc.get("big"):
            top = f'<p style="font-size:64px; font-weight:700; line-height:1.1">{esc(sc["big"])}</p>' + ptext(sc["label"], 26, color=MUTED)
        else:
            top = (f'<div style="width:72px; height:72px; background:{NAVY}; border-radius:36px; display:flex; flex-direction:row; align-items:center; justify-content:center">'
                   f'<x-icon name="CheckCircle" style="width:40px; height:40px; color:{LIME}"></x-icon></div>')
        cols.append(col(h3(sc["heading"]) + top + ptext(sc["text"], 32, 1.45)))
    inner = row("\n".join(cols), gap=48) + "\n" + ptext(f"Source: {pl['source']}", 24, color=MUTED)
    body = title(c.get("situation_title") or f"Why {c['use_case_short']} get blocked today", eyebrow=eb(c)) + "\n" + fill(inner, 48)
    notes = (f"At {n(c['volume'])} a day the volume is {c['volume']/pl['recipients_per_day']:.0f} times the {n(pl['recipients_per_day'])}-recipient daily limit of a single mailbox. "
             "That is why the provider throttles or blocks the traffic.")
    return dict(bg=CREAM, body=body, notes=notes, gap=32)

def s_approach(c):
    L = card(pill(f"Inbound · stays on {c['provider']}", GREEN, POSITIVE_INK, 26, 600, "8px 22px") +
             h3("No change at the front door") +
             chips(["Customer", c["provider"], "Workspace"], GREEN, POSITIVE_INK, INK) +
             ul(["MX records stay as they are", "Customers write to the same address",
                 "One shared mailbox receives all mail", "Agents keep their current workflow"]), pad=40, gap=20)
    R = card(pill("Outbound · moves to MailerCloud", LIME, NAVY, 26, 600, "8px 22px") +
             h3("A route built for volume", color=CARD) +
             chips(["Workspace", "MailerCloud", "Inbox"], LIME, NAVY, CARD) +
             ul(["Sent by MailerCloud SMTP or Email API", f"Signed with {c['client']}'s own domain",
                 f"Sized for {n(c['volume'])} a day and more", "Reply-To points back to the mailbox"], color=CARD),
              dark=True, pad=40, gap=20)
    body = title("One mailbox in, MailerCloud out", eyebrow=eb(c)) + "\n" + fill(row(L + "\n" + R))
    notes = ("This is the whole idea on one slide. Inbound: MX stays where it is and the shared mailbox keeps receiving customer emails. "
             f"Outbound: every reply is sent through MailerCloud, authenticated with {c['client']}'s own domain. Customers and agents notice no change at the front door; only the outbound route is new.")
    return dict(bg=MINT, body=body, notes=notes, gap=32)

def s_architecture(c):
    prov = esc(c["provider"])
    p32 = lambda t: f'<p style="font-size:32px; font-weight:700; line-height:1.4">{t}</p>'
    p26 = lambda t: f'<p style="font-size:26px; line-height:1.4">{t}</p>'
    parts = ["<!-- Nodes (left, top, w, h): A 128,352,400,476 | B1 760,352,400,196 | C 1392,352,400,476 | B2 760,632,400,196. Arrow rows y=450 and y=730 -->",
             title("Inbound stays put, outbound moves", eyebrow=eb(c)),
             f'<p style="position:absolute; left:760px; top:300px; width:400px; background:{CARD}; color:{INK}; border:3px solid {INK}; border-radius:30px; font-size:24px; font-weight:700; letter-spacing:1px; line-height:1.2; padding:6px 20px; text-align:center; text-transform:uppercase">Inbound · No change</p>',
             f'<p style="position:absolute; left:760px; top:580px; width:540px; background:{NAVY}; color:{LIME}; border:3px solid {NAVY}; border-radius:30px; font-size:24px; font-weight:700; letter-spacing:1px; line-height:1.2; padding:6px 20px; text-align:center; text-transform:uppercase">Outbound · Via MailerCloud</p>',
             node(128, 352, 400, 476, p32("Customers") + p26("Gmail, Outlook, Yahoo, corporate mail") + p26("Write to the support address") + p26(f"Get replies from {esc(c['client'])}'s domain"), pad="108px 28px 28px"),
             node(760, 352, 400, 196, p32(prov) + f'<p style="font-size:24px; line-height:1.4">{esc(c["inbound_note"])}</p>', pad="64px 28px 12px", gap=4),
             node(1392, 352, 400, 476, p32(esc(c["workspace"])) + p26(esc(c["workspace_sub"])) + p26("Agents read and reply here") + p26("Sends each reply to MailerCloud"), pad="108px 28px 28px"),
             node(760, 632, 400, 196, f'<p style="font-size:32px; font-weight:700; line-height:1.4; color:{CARD}">MailerCloud</p><p style="font-size:24px; line-height:1.4; color:{LIGHT_ON_NAVY}">SMTP relay or Email API, signed and logged</p>', dark=True, pad="64px 28px 12px", gap=4),
             icon("Globe", 156, 380, 56), icon("Chat", 788, 370, 44), icon("Users", 1420, 380, 56), icon("PaperPlane", 788, 650, 44, LIME),
             conn(528, 450, 760, 450), conn(1160, 450, 1392, 450),
             conn(1392, 730, 1160, 730, BLUE, 6), conn(760, 730, 528, 730, BLUE, 6),
             pin_p(536, 370, 216, "<b>1</b> Customer<br>writes in"), pin_p(1168, 370, 216, "<b>2</b> Synced to<br>the workspace"),
             pin_p(1168, 650, 216, "<b>3</b> Agent reply<br>by SMTP or API"), pin_p(536, 650, 216, "<b>4</b> Signed reply<br>to the inbox"),
             pin_p(128, 846, 1664, f"Reply-To points to the shared mailbox, so customer answers return to {prov}.", 26, 400, "left", MUTED)]
    notes = (f"Inbound stays on {c['provider']}; outbound replies are routed through MailerCloud. Read the loop clockwise from the top left. 1: the customer writes to the support address. 2: the shared mailbox holds it and the support workspace picks it up. "
             "3: the agent's reply goes to MailerCloud by SMTP or API. 4: MailerCloud delivers a signed reply to the customer's inbox.")
    return dict(bg=LIME, body="\n".join(parts), notes=notes, gap=16)

def s_dataflow(c):
    xs = [128, 563, 997, 1432]; cx = [x + 180 for x in xs]
    actors = [("Customer", "Any mailbox provider", False), (c["provider"], "Shared support mailbox", False),
              (c["workspace"], c["workspace_sub_short"], False), ("MailerCloud", "SMTP relay / Email API", True)]
    parts = ["<!-- Actors: 128/563/997/1432, top 300, 360x96. Arrow rows y: 452, 540, 628, 716, 804 -->",
             title("Five steps from question to status", eyebrow=eb(c))]
    for x in xs:
        parts.append(f'<div style="position:absolute; left:{x}px; top:396px; width:360px; height:484px; background:rgba(253,253,248,0.3); border-radius:0 0 28px 28px"></div>')
    for x, (a, b, dark) in zip(xs, actors):
        bg, fg1, fg2 = (NAVY, CARD, LIGHT_ON_NAVY) if dark else (CARD, INK, INK)
        bd = NAVY if dark else INK
        parts.append(f'<div style="position:absolute; left:{x}px; top:300px; width:360px; height:96px; background:{bg}; border:3px solid {bd}; border-radius:28px 28px 0 0; display:flex; flex-direction:column; justify-content:center; padding:8px 20px">'
                     f'<p style="font-size:28px; font-weight:700; line-height:1.25; text-align:center; color:{fg1}">{esc(a)}</p>'
                     f'<p style="font-size:24px; line-height:1.25; text-align:center; color:{fg2}">{esc(b)}</p></div>')
    A, B, C, D = cx
    arrows = [(A, B, INK, 4, False), (B, C, INK, 4, False), (C, D, NAVY, 6, False), (D, A, NAVY, 6, False), (D, C, NAVY, 4, True)]
    for i, (x1, x2, col_, w, dash) in enumerate(arrows): parts.append(conn(x1, 452 + 88 * i, x2, 452 + 88 * i, col_, w, dash))
    labels = [("1 · Email reaches mailbox", "Standard SMTP to your MX", A, 435), ("2 · Ticket is created", "Helpdesk mailbox connector", B, 434),
              ("3 · Agent reply sent", "SMTP relay or Email API call", C, 435), ("4 · Signed delivery to the inbox", "SPF, DKIM and DMARC aligned", None, 500),
              ("5 · Status webhooks return", "Delivered, bounced, complaint", C, 435)]
    for i, (top, sub, x, w) in enumerate(labels):
        y = 452 + 88 * i
        left = 710 if x is None else x
        parts.append(pin_p(left, y - 40, w, esc(top), 24, 600, lh=1.25))
        parts.append(pin_p(left, y + 10, w, esc(sub), 24, 400, color=MUTED, lh=1.25))
    notes = ("Walk the arrows top to bottom. Solid dark lines are inbound and stay where they are. Navy lines are the new outbound path; the dashed line is delivery status returning to the workspace by webhook. "
             "When the customer answers, the reply goes back to the same shared mailbox and the loop starts again at step 1.")
    return dict(bg=SKY, body="\n".join(parts), notes=notes, gap=16)

def s_integration(c):
    def kv(key, val): return f'<span style="color:{CODE_KEY}">"{key}"</span>: <span style="color:{CODE_STR}">"{val}"</span>'
    nb = "&#160;"
    code = (f'{{<br>\n{nb*2}<span style="color:{CODE_KEY}">"email"</span>: {{<br>\n'
            f'{nb*4}{kv("from", "support@"+esc(c["client_domain"]))},<br>\n{nb*4}{kv("subject", "Re: Your support request")},<br>\n'
            f'{nb*4}<span style="color:{CODE_KEY}">"recipients"</span>: {{<br>\n{nb*6}<span style="color:{CODE_KEY}">"to"</span>: [{{ {kv("email","customer@example.com")} }}]<br>\n{nb*4}}}<br>\n{nb*2}}},<br>\n'
            f'{nb*2}<span style="color:{CODE_KEY}">"metadata"</span>: {{<br>\n{nb*4}{kv("campaignType","TRANSACTIONAL")},<br>\n{nb*4}{kv("messageId","3f9c2c6e-1b7e-4f3a")}<br>\n{nb*2}}}<br>\n}}')
    mono = f"color:{CODE_TXT}; font-family:{MONO}; font-size:24px"
    left = ('<div style="width:640px; display:flex; flex-direction:column; gap:24px">\n'
            + card(h3("Option A: SMTP relay") + ptext("For a helpdesk with custom outgoing mail settings. Swap the host, port and credentials; agents change nothing.", 26), pad=32, gap=12, flex=False) + "\n"
            + card(h3("Option B: Email API") + ptext("For a custom-built system. One REST call per reply, with ticket metadata, tags and safe retries.", 26), pad=32, gap=12, flex=False) + "\n</div>")
    right = (f'<div style="flex:1; display:flex; flex-direction:column; gap:16px; background:{NAVY}; padding:28px 36px; border-radius:28px; box-shadow:{SH_DARK}">\n'
             f'<div style="display:flex; flex-direction:row; gap:16px; align-items:center">'
             f'<p style="background:#7be0a8; color:{POSITIVE_INK}; font-family:{MONO}; font-size:24px; font-weight:700; line-height:1.3; padding:6px 18px; border-radius:12px">POST</p>'
             f'<p style="{mono}; line-height:1.3">email-api.mailercloud.com/email</p></div>\n'
             f'<hr style="border-top:2px solid {NAVY_LINE}">\n<p style="{mono}; line-height:1.25">{code}</p>\n<hr style="border-top:2px solid {NAVY_LINE}">\n'
             f'<div style="display:flex; flex-direction:row; gap:16px; align-items:center"><p style="background:{POSITIVE_BG}; color:{POSITIVE_INK}; font-size:24px; font-weight:700; line-height:1.3; padding:6px 18px; border-radius:12px">200 OK</p>'
             f'<p style="color:{CARD}; font-size:26px; line-height:1.3">Email accepted</p></div>\n</div>')
    body = title("Two ways to connect", eyebrow=eb(c)) + "\n" + fill(row(left + "\n" + right, 48))
    notes = ("Both paths do the same job. If the helpdesk has custom outgoing SMTP settings, option A is a settings change and nothing else. If the support tool is built in-house, option B is one REST call per reply. "
             "The messageId is the ticket-reply identifier: a messageId reused within 24 hours is never sent twice, so a retry cannot double-send. The payload is illustrative; sender address and content are placeholders.")
    return dict(bg=PINK, body=body, notes=notes, gap=32)

def s_auth(c):
    rows = [("SPF", "Allows MailerCloud to send", "Add MailerCloud to your SPF record"),
            ("DKIM", "Signs every reply", "Publish the DKIM keys from MailerCloud"),
            ("DMARC", "Sets the policy for failed mail", "Start at p=none, then tighten to reject"),
            ("Bounce domain", "Routes bounces, aligns SPF", "Point a bounce subdomain to MailerCloud")]
    inner = open_rows(["Record", "What it does", "What changes"], [16, 34, 50], rows, 28, callout=("MX", f"No change. Inbound stays on {c['provider']}."))
    body = title("Four DNS records, MX unchanged", eyebrow=eb(c)) + "\n" + fill(inner)
    notes = ("Four records for outbound, none for inbound. The MX row is the reassurance: customers still reach the inbound system exactly as before. Check the current SPF record for the 10-lookup limit before adding the MailerCloud include. "
             "Decision for the call: send from the main domain or from a dedicated subdomain, which keeps support-mail reputation separate from corporate mail.")
    return dict(bg=CREAM, body=body, notes=notes, gap=32)

def s_capacity(c):
    per_min = int(c["volume"] / (c["window_hours"] * 60) + 0.5)   # 62.5 -> 63
    lim = c["provider_limits"]["messages_per_min"]
    w_need = 780; w_lim = max(120, min(w_need, round(w_need * lim / per_min)))
    left = ('<div style="width:800px; display:flex; flex-direction:column; gap:40px">\n'
            f'<div style="display:flex; flex-direction:column; gap:8px">\n<p style="font-size:88px; font-weight:700; line-height:1.1">{n(c["volume"])}</p>\n'
            + ptext(f"replies a day, about {per_min} a minute over a support day of {c['window_hours']} hours.") + "\n</div>\n"
            '<div style="display:flex; flex-direction:column; gap:28px">\n'
            f'<div style="display:flex; flex-direction:column; gap:12px">\n<p style="font-size:26px; font-weight:600; line-height:1.3">What {esc(c["client"])} needs: about {per_min} a minute</p>\n<div style="width:{w_need}px; height:56px; background:{NAVY}; border-radius:28px"></div>\n</div>\n'
            f'<div style="display:flex; flex-direction:column; gap:12px">\n<p style="font-size:26px; font-weight:600; line-height:1.3">{esc(c["provider"])} limit: {lim} a minute per mailbox</p>\n<div style="width:{w_lim}px; height:56px; background:{CARD}; border:3px solid {INK}; border-radius:28px"></div>\n</div>\n</div>\n</div>')
    right = ('<div style="flex:1; display:flex; flex-direction:column; gap:24px">\n'
             + card(h3("Shared pool, Good tier") + ptext("Fastest start. Reputation is already established, which suits clean, reply-only traffic.", 26), pad=36, gap=12, flex=False) + "\n"
             + card(h3("Dedicated IP") + ptext("Full control. Your own reputation, isolated from other senders. Needs a short warm-up.", 26), pad=36, gap=12, flex=False) + "\n</div>")
    body = title("Capacity and IP choice", eyebrow=eb(c)) + "\n" + fill(row(left + "\n" + right, 64, "; align-items:center"))
    notes = (f"The {per_min} a minute figure assumes all {n(c['volume'])} replies go out within {c['window_hours']} hours ({n(c['volume'])} / {c['window_hours']*60} minutes). Spread over 24 hours it is about {c['volume']/1440:.0f} a minute, "
             f"but a single mailbox would still reach its {n(c['provider_limits']['recipients_per_day'])}-recipient daily limit first. Ask for the real peak hourly volume. Shared pool versus dedicated IP is a decision for the call; a dedicated IP needs a few days of warm-up for a domain that already sends.")
    return dict(bg=GREEN, body=body, notes=notes, gap=32)

def s_warmup(c):
    r = c["ramp"]; m = max(r); cnt = len(r)
    w = int((896 - 32 * (cnt - 1)) / cnt)
    cols = []
    for i, v in enumerate(r):
        last = i == cnt - 1
        hgt = round(340 * v / m); col = BLUE if last else NAVY
        lab = f"Day {i+1} onward" if last else f"Day {i+1}"
        cols.append(f'<div style="width:{w}px; display:flex; flex-direction:column; gap:12px">\n<p style="font-size:26px; font-weight:700; line-height:1.3; text-align:center">{k(v)}</p>\n'
                    f'<div style="height:{hgt}px; background:{col}; border-radius:16px 16px 0 0"></div>\n<p style="font-size:26px; line-height:1.3; text-align:center">{lab}</p>\n</div>')
    chart = '<div style="display:flex; flex-direction:row; gap:32px; align-items:flex-end">\n' + "\n".join(cols) + "\n</div>"
    rules = card(h3("Rules for the ramp", color=CARD) + ul(["Send to recent, engaged contacts first", "Review Gmail and Outlook delivery every day",
                 "Hold the step if bounces or complaints rise", "The domain's sending history is what makes a fast ramp realistic"], 26, CARD), dark=True, pad=36, gap=16, extra="; align-self:center")
    body = (title(c["ramp_title"], "Emails per day, adjusted daily to what Gmail and Outlook show.", eyebrow=eb(c)) +
            "\n" + fill('<div style="display:flex; flex-direction:row; gap:64px; align-items:center">\n' + chart + "\n" + rules + "\n</div>"))
    notes = (f"Each bar is the planned volume for that day: {', '.join(k(v) for v in r[:-1])}, then {k(m)} from day {cnt}. The ramp can be this fast because {c['client']} already sends regularly, so the domain has sending history. "
             "A new dedicated IP still has no reputation of its own, so keep the first days on the most engaged recipients and hold a step if Gmail or Outlook show deferrals or spam placement. A shared pool skips the ramp entirely.")
    return dict(bg=LIME, body=body, notes=notes, gap=32)

def s_control(c):
    items = [("Delivery logs", "Status of every reply, by message and recipient.", CARD),
             ("Status webhooks", "Bounces and complaints return to the helpdesk.", CARD),
             ("Suppression list", "Dead addresses are suppressed, not retried.", CARD),
             ("Safe retries", "A repeated messageId within 24 hours is never sent twice.", CARD),
             ("Inbox Tracker", "Inbox, Spam or Undelivered, across Gmail, Yahoo and more.", CARD),
             ("One-to-one mail", "Tracking off, so replies read as personal.", LIME)]
    tiles = "\n".join(f'<div style="display:flex; flex-direction:column; gap:12px; background:{bg}; padding:32px; border-radius:28px; box-shadow:{SH}">\n{h3(a, 32)}\n{ptext(b, 26)}\n</div>' for a, b, bg in items)
    grid = f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:32px">\n{tiles}\n</div>'
    body = title("Every reply has a status", eyebrow=eb(c)) + "\n" + fill(grid)
    notes = ("This is what the support team gets that the current setup could not give them: a status for every reply, failures that show up on the ticket, and safe retries. Status webhooks post delivered, bounced and complaint events back to the helpdesk. The last tile is a setup recommendation rather than a product limit: open and click tracking stay off for one-to-one support replies.")
    return dict(bg=MINT, body=body, notes=notes, gap=32)

def s_rollout(c):
    rows = []
    for st in c["rollout"]:
        rows.append(f'<div style="display:flex; flex-direction:row; align-items:center; gap:32px; padding:18px 0px; border-bottom:{hair()}">'
                    f'<p style="width:190px; background:{CARD}; color:{INK}; font-size:24px; font-weight:700; line-height:1.3; padding:8px 0px; border-radius:30px; text-align:center">{esc(st["when"])}</p>'
                    f'<p style="width:380px; font-size:32px; font-weight:700; line-height:1.2">{esc(st["title"])}</p>'
                    f'<p style="flex:1; font-size:26px; line-height:1.4">{esc(st["text"])}</p></div>')
    inner = '<div style="display:flex; flex-direction:column">\n' + "\n".join(rows) + "\n</div>\n" + ptext(c["rollout_banner"], 26, color=MUTED, weight=600)
    body = title(c["rollout_title"], eyebrow=eb(c)) + "\n" + fill(inner, 32)
    notes = ("DNS and integration take a few days, then volume ramps within the first week because the domain already has sending history. The second week holds full volume while placement is confirmed. Timings assume DNS changes can be made quickly, which is one of the questions for the call.")
    return dict(bg=SKY, body=body, notes=notes, gap=32)

def s_risks(c):
    inner = open_rows(["Risk", "How we manage it"], [38, 62], c["risks"], 28)
    body = title("Risks and how we manage them", eyebrow=eb(c)) + "\n" + fill(inner)
    notes = "Name the risks before the client does. Each one has a concrete response, and none of them blocks the plan; the DNS and helpdesk items are the ones to confirm on the call."
    return dict(bg=LIME, body=body, notes=notes, gap=32)

def s_proof(c):
    stats = []
    for i, (fig, lab) in enumerate(c["proof_stats"]):
        pad = "0px 32px 0px 0px" if i == 0 else ("0px 32px 0px 40px" if i < len(c["proof_stats"]) - 1 else "0px 0px 0px 40px")
        bd = "" if i == 0 else f"; border-left:3px solid {INK}"
        stats.append(f'<div style="flex:1; display:flex; flex-direction:column; gap:4px; padding:{pad}{bd}">\n<p style="font-size:64px; font-weight:700; line-height:1.1">{esc(fig)}</p>\n{ptext(lab, 26)}\n</div>')
    cs = [card(pill(t, SKY if i else LIME) + h3(nm) + ptext(tx, 26), pad=36, gap=14) for i, (t, nm, tx, *_) in enumerate(c["cases"])]
    inner = ('<div style="display:flex; flex-direction:row; gap:0px">\n' + "\n".join(stats) + "\n</div>\n" + row("\n".join(cs)) +
             "\n" + ptext("Source: mailercloud.com (homepage) and the MailerCloud company overview for the case studies.", 24, color=MUTED))
    body = title("Proven at scale", eyebrow=eb(c)) + "\n" + fill(inner, 40)
    notes = ("Two customers with the same root problem. Turtle was capped by its previous provider and had customers not receiving mail; RedBus had shared infrastructure and incomplete DNS. The headline figures come from the mailercloud.com homepage; re-check them before each new deck.")
    return dict(bg=PINK, body=body, notes=notes, gap=32)

def s_security(c):
    items = [("Lock", "Encryption", "Data is encrypted in transit and at rest.", LIME),
             ("Verified", "Global standards", "ISO/IEC 27001:2022, GDPR compliant, VAPT certified.", SKY),
             ("Trust", "Privacy regulations", "Compliant with GDPR, CAN-SPAM and CASL.", MINT),
             ("Key", "Access control", "Role-based access and multi-factor authentication.", PINK),
             ("Activity", "Monitoring", "Real-time monitoring and an incident response plan.", CREAM),
             ("Database", "Resilience", "Monitored data centres, backups and continuity tests.", GREEN)]
    tiles = "\n".join(f'<div style="display:flex; flex-direction:column; gap:14px; background:{bg}; padding:32px; border-radius:28px; box-shadow:8px 8px 0 rgba(2,10,19,0.12)">\n'
                      f'<div style="display:flex; flex-direction:row; align-items:center; gap:16px"><div style="width:56px; height:56px; background:{CARD}; border-radius:28px; display:flex; flex-direction:row; align-items:center; justify-content:center"><x-icon name="{ic}" style="width:32px; height:32px; color:{NAVY}"></x-icon></div>{h3(a, 32)}</div>\n'
                      f'{ptext(b, 26)}\n</div>' for ic, a, b, bg in items)
    body = title("Security and compliance", eyebrow=eb(c)) + "\n" + fill(f'<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:32px">\n{tiles}\n</div>')
    notes = "Six points that IT and compliance teams usually ask about, from the MailerCloud company overview and the certifications on mailercloud.com. If the client has a security questionnaire, hand it over alongside this slide."
    return dict(bg=PAPER, body=body, notes=notes, gap=32)

def s_next(c):
    L = card(h3("To agree on this call") + ul(c["decisions"], 32, tag="ol"), pad=40, gap=16)
    R = card(h3("Next steps", color=LIME) + ul(c["next_steps"], 32, CARD, tag="ol"), dark=True, pad=40, gap=16)
    body = title("Decisions and next steps", eyebrow=eb(c)) + "\n" + fill(row(L + "\n" + R))
    notes = "Use the left card as the discovery checklist and get an answer to each item before the call ends. The answers decide the integration path, the sending identity, the IP option and the DNS timeline. The right card is what happens the day after."
    return dict(bg=LIME, body=body, notes=notes, gap=32)

def s_appendix(c):
    gl = [("SPF", "who may send for a domain"), ("DKIM", "a signature proving mail is genuine"), ("DMARC", "what to do when the checks fail"),
          ("MX", "where incoming mail is delivered"), ("Hard bounce", "a permanent delivery failure"), ("Warm-up", "raising volume in steps")]
    per_min = int(c["volume"] / (c["window_hours"] * 60) + 0.5)
    ass = [f"{n(c['volume'])} one-to-one {c['use_case_short']} a day", f"About {per_min} a minute if sent within {c['window_hours']} hours",
           f"{c['provider']} stays the inbound system", "Sending domain decided on the call", "Warm-up figures are indicative"]
    gl_html = "\n".join(f'<p style="font-size:26px; line-height:1.4"><b>{esc(a)}</b>: {esc(b)}</p>' for a, b in gl)
    L = card(h3("Glossary") + gl_html, pad=36, gap=18)
    R = card(h3("Assumptions") + ul(ass, 26), pad=36, gap=16)
    body = title("Appendix: glossary and assumptions", eyebrow=eb(c)) + "\n" + fill(row(L + "\n" + R))
    notes = "Reference only. Leave this slide out of the live walk-through and use it when a question needs a definition or an assumption checked."
    return dict(bg=CREAM, body=body, notes=notes, gap=32)

def s_closing(c):
    adr = [("London", "Hamilton House, Mabledon Place, London, Greater London, WC1H 9BB, United Kingdom"),
           ("Kerala", "1/213, BR Building, Iringalloor, Ammathoorpadam, Guruvayurappan College PO, Kozhikode, Kerala, India - 673014"),
           ("Bangalore", "HQ BL Commerce G01, 125, 7th Cross Road, Opposite TG Citadel, Off Bannerghatta Main Road, Dollar Layout Btm 2nd Stage, Bilekahalli, Bangalore Karnataka 560076, India")]
    cols = "\n".join(f'<div style="flex:1; display:flex; flex-direction:column; gap:8px">\n<p style="font-size:32px; font-weight:700; line-height:1.3">{a}</p>\n<p style="font-size:24px; line-height:1.4">{b}</p>\n</div>' for a, b in adr)
    body = (f'<div style="position:absolute; left:1500px; top:140px; width:260px; height:260px; background:{LIME}; border-radius:130px"></div>\n'
            f'<div style="position:absolute; left:1380px; top:300px; width:160px; height:160px; background:{GREEN}; border-radius:80px"></div>\n'
            '<div style="flex:1"></div>\n<h1 style="font-size:88px; font-weight:700; line-height:1.1">Thank you</h1>\n' +
            ptext(f"Support replies through MailerCloud, inbound mail on {c['provider']}.", 32, extra="; width:1100px") +
            '\n<div style="flex:1"></div>\n' + row(cols, 48))
    notes = "Close by restating the outcome: customers and agents notice no change at the front door, and the volume leaves on a route built for it. Confirm the answers to the decision list and agree a date for the DNS and integration work."
    return dict(bg=SKY, body=body, notes=notes, gap=32)

ORDER = [("cover", s_cover, None), ("summary", s_exec, "Summary"), ("situation", s_situation, "Context"), ("approach", s_approach, "Context"),
         ("architecture", s_architecture, "Design"), ("dataflow", s_dataflow, "Design"), ("integration", s_integration, "Design"), ("authentication", s_auth, "Design"),
         ("capacity", s_capacity, "Operate"), ("warmup", s_warmup, "Operate"), ("control", s_control, "Operate"), ("rollout", s_rollout, "Operate"), ("risks", s_risks, "Operate"),
         ("proof", s_proof, "Proof"), ("security", s_security, "Proof"), ("nextsteps", s_next, "Next steps"), ("appendix", s_appendix, "Next steps"), ("closing", s_closing, None)]

def footer(i, total, label):
    mid = esc(label) if label else "&#160;"
    st = f"font-size:24px; color:{MUTED}"
    return (f'<div style="position:absolute; left:128px; bottom:64px; width:1664px; height:34px; display:flex; flex-direction:row">'
            f'<p style="flex:1; {st}">www.mailercloud.com</p><p style="flex:1; {st}; text-align:center">&#160;</p>'
            f'<p style="flex:1; {st}; text-align:right">{i:02d} / {total:02d}</p></div>')

def assemble(c, logo):
    total = len(ORDER); out = {}
    for i, (sid, fn, label) in enumerate(ORDER, 1):
        c['_section'] = label
        d = fn(c)
        logo_tag = f'<img src="{logo}" alt="MailerCloud" style="position:absolute; left:128px; top:56px; width:220px; height:45px; object-fit:contain">'
        if d.get("cover"):
            foot = f'<p style="position:absolute; left:128px; bottom:64px; width:600px; font-size:24px; color:{MUTED}">www.mailercloud.com</p>'
        elif sid == "closing":
            foot = footer(i, total, None)
        else:
            foot = footer(i, total, label)
        pad = "128px 128px 160px" if (d.get("cover") or sid == "closing") else "152px 128px 200px"
        style = (f"background:{d['bg']}; color:{INK}; font-family:{FONT}; padding:{pad}; display:flex; "
                 f"flex-direction:{d.get('direction','column')}; gap:{d.get('gap',40)}px" + (f"; justify-content:{d['justify']}" if d.get("justify") else ""))
        body = d["body"]
        # decor (pinned, first) must precede flow content, logo/footer can follow
        html_ = f'<section id="{sid}" data-transition="fade" style="{style}">\n{body}\n{logo_tag}\n{foot}\n<aside>{esc(d["notes"])}</aside>\n</section>\n'
        out[sid] = html_
    return out

SECTIONS = {"cover": "Why support replies are blocked today, the approach and the summary",
            "architecture": "The design: architecture, data flow, integration paths and domain authentication",
            "capacity": "Running it: capacity, warm-up, controls, rollout and risks",
            "proof": "Proof, security and the decisions for the call"}

def deck_json(c):
    return {"v": 4, "createdOnFiles": {"v": 1, "at": "2026-09-24T09:00:00Z"}, "title": f"{c['client']} × MailerCloud: {c['deck_title']}",
            "order": [s[0] for s in ORDER],
            "sections": {f"s{i+1}": {"description": d, "start": sid} for i, (sid, d) in enumerate(SECTIONS.items())},
            "faces": {"poppins": {"family": "Poppins", "href": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"},
                      "jetbrains-mono": {"family": "JetBrains Mono", "href": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap"}},
            "designSystems": []}

# ------------------------------------------------------------------ lint ----
def lint(slides, c):
    problems = []
    for sid, h in slides.items():
        for m in re.finditer(r"font-size:(\d+)px", h):
            if int(m.group(1)) < 24: problems.append(f"{sid}: font-size {m.group(1)}px is below the 24px floor")
        t = re.search(r"<h2[^>]*>(.*?)</h2>", h)
        if t and len(html.unescape(t.group(1))) > 40: problems.append(f"{sid}: title is {len(html.unescape(t.group(1)))} characters (max 40 to stay on one line)")
        if h.count("<section") != 1 or not h.strip().endswith("</section>"): problems.append(f"{sid}: must contain exactly one section")
        if "#000000" in h or "#ffffff" in h.lower(): problems.append(f"{sid}: pure black or white used; use tokens")
        if "<aside>" not in h: problems.append(f"{sid}: missing speaker notes")
        for m in re.finditer(r'left:(\d+)px; top:(\d+)px; width:(\d+)px; height:(\d+)px', h):
            l, tp, w, hh = map(int, m.groups())
            if l + w > 1920 or tp + hh > 1080: problems.append(f"{sid}: pinned box leaves the 1920x1080 canvas")
    return problems

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("config"); ap.add_argument("out")
    ap.add_argument("--logo", default="/_blob/REPLACE_WITH_LOGO_ASSET_ID")
    a = ap.parse_args()
    c = json.load(open(a.config))
    slides = assemble(c, a.logo)
    probs = lint(slides, c)
    sd = os.path.join(a.out, "project", "slides"); os.makedirs(sd, exist_ok=True)
    for sid, h in slides.items(): open(os.path.join(sd, sid + ".html"), "w").write(h)
    json.dump(deck_json(c), open(os.path.join(a.out, "project", "deck.json"), "w"), indent=2, ensure_ascii=False)
    print(f"built {len(slides)} slides into {a.out}")
    if probs:
        print("LINT:"); [print("  -", p) for p in probs]; sys.exit(1)
    print("lint clean")

if __name__ == "__main__": main()
