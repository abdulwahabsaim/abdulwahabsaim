#!/usr/bin/env python3
"""
Builds the self-hosted SVGs used by README.md (light and dark versions).

    python3 scripts/build_assets.py

Edit the DATA section when a lab count, status or line changes, then rerun.
No third-party services: every image in the README header, cards, dividers and footer comes from here.
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

# ---------------------------------------------------------------- DATA
TERMINAL = [
    ("cmd", "whoami"),
    ("out", [("Abdul Wahab Saim", "strong"), ("  junior network engineer, ", "muted"), ("CCNA 200-301", "accent")]),
    ("cmd", "ls labs"),
    ("out", [("routing/  security/  services/  firewall/  ", "dir"), ("campus", "plain")]),
    ("cmd", "cat status.txt"),
    ("out", [("available full-time", "plain"), ("   based in Goes, NL", "muted"), ("   open to relocating", "muted")]),
]

CARDS = [
    # slug, kicker, title, number, unit, tags, wide
    ("campus", "Flagship", "Enterprise campus network", "15", "devices",
     "Multi-area OSPFv2, HSRPv2, EtherChannel, DHCP Snooping and DAI, WLC, dual-ISP failover", True),
    ("routing", "enterprise-routing-labs", "Routing", "13", "labs",
     "OSPF, EIGRP, HSRP, NAT and PAT, QoS, GRE, IPv6", False),
    ("security", "layer2-security-labs", "Layer 2 and security", "13", "labs",
     "VLANs, STP guards, EtherChannel, DAI, ACLs, SSHv2", False),
    ("services", "network-services-labs", "Network services", "5", "labs",
     "DHCP relay, DNS, NTP, Syslog, Cisco 3504 WLC", False),
    ("firewall", "cisco-asa-firewall-labs", "Cisco ASA firewalls", "3", "labs, in progress",
     "Security levels, ACLs and object groups, NAT, DMZ", False),
]

# ---------------------------------------------------------------- THEME
ACCENT = "#ff6a1f"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
THEMES = {
    "light": dict(bg="#ffffff", card="#ffffff", line="#d1d9e0", text="#1f2328", text2="#59636e", text3="#818b98",
                  dot="rgba(31,35,40,0.14)", accent_text="#c2410c"),
    "dark": dict(bg="#0d1117", card="#151b23", line="#3d444d", text="#e6edf3", text2="#9198a1", text3="#6e7681",
                 dot="rgba(230,237,243,0.16)", accent_text="#ff8a4c"),
}


def svg(w, h, label, body, css):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title><style>{css}</style>{body}</svg>\n')


# ---------------------------------------------------------------- TERMINAL (dark window in both themes)
def terminal():
    W, FS, CW, LH = 1000, 17, 10.25, 30  # CW: approx monospace char width at FS
    PAD_X, TOP = 34, 86
    PROMPT = "visitor@saim:~$ "
    rows, t = [], 0.4
    css = [f"""
      .win{{fill:#0f0f11}} .bar{{fill:#18181b}}
      text{{font:400 {FS}px {MONO};white-space:pre}}
      .prompt{{fill:{ACCENT}}} .cmd{{fill:#ffffff;font-weight:600}}
      .strong{{fill:#ffffff;font-weight:600}} .muted{{fill:#8c8c96}} .accent{{fill:{ACCENT}}}
      .dir{{fill:#8ab4ff;font-weight:600}} .plain{{fill:#e6e6ea}} .title{{fill:#8c8c96;font-size:14px}}
      .cover{{fill:#0f0f11}}
      .cursor{{fill:{ACCENT};animation:hide 0s linear backwards, blink 1s steps(1) infinite}}
      @keyframes hide{{from{{opacity:0}}}}
      @keyframes blink{{50%{{opacity:0}}}}
      @keyframes fade{{from{{opacity:0}}}}
    """]
    y = TOP
    for i, (kind, val) in enumerate(TERMINAL):
        if kind == "cmd":
            n = len(val)
            dur = 0.07 * n
            x0 = PAD_X + len(PROMPT) * CW
            rows.append(f'<text x="{PAD_X}" y="{y}" class="row r{i}"><tspan class="prompt">{escape(PROMPT)}</tspan>'
                        f'<tspan class="cmd">{escape(val)}</tspan></text>')
            # A cover slides right in steps, revealing the command one character at a time.
            rows.append(f'<rect x="{x0 - 1:.1f}" y="{y - FS}" width="{n * CW + 6:.1f}" height="{FS + 8}" class="cover c{i}"/>')
            # Default state is fully revealed (cover moved aside), so a static render shows everything.
            css.append(f".r{i}{{animation:fade .01s linear {t:.2f}s backwards}}"
                       f".c{i}{{transform:translateX({n * CW + 6:.1f}px);animation:type{i} {dur:.2f}s steps({n}) {t + 0.25:.2f}s backwards}}"
                       f"@keyframes type{i}{{from{{transform:translateX(0)}}}}")
            t += 0.25 + dur + 0.35
        else:
            spans = "".join(f'<tspan class="{c}">{escape(s)}</tspan>' for s, c in val)
            rows.append(f'<text x="{PAD_X}" y="{y}" class="row r{i}">{spans}</text>')
            css.append(f".r{i}{{animation:fade .25s ease-out {t:.2f}s backwards}}")
            t += 0.55
            y += 12  # breathing room after output
        y += LH
    cy = y
    rows.append(f'<text x="{PAD_X}" y="{cy}" class="row rl"><tspan class="prompt">{escape(PROMPT)}</tspan></text>')
    rows.append(f'<rect x="{PAD_X + len(PROMPT) * CW:.1f}" y="{cy - FS + 2}" width="10" height="{FS + 2}" class="cursor"/>')
    css.append(f".rl{{animation:fade .01s linear {t:.2f}s backwards}}"
               f".cursor{{animation-delay:{t:.2f}s,{t:.2f}s}}")
    css.append("@media (prefers-reduced-motion:reduce){.row,.cover,.cursor{animation:none!important}}")
    H = cy + 40
    body = (f'<rect class="win" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" stroke="rgba(255,255,255,0.08)"/>'
            f'<path class="bar" d="M18.5 .5 H{W - 18.5} A18 18 0 0 1 {W - .5} 18.5 V46 H.5 V18.5 A18 18 0 0 1 18.5 .5 Z"/>'
            f'<circle cx="30" cy="23" r="6.5" fill="{ACCENT}"/><circle cx="52" cy="23" r="6.5" fill="#3a3a40"/>'
            f'<circle cx="74" cy="23" r="6.5" fill="#3a3a40"/><text x="100" y="28" class="title">saim-shell</text>'
            + "".join(rows))
    return svg(W, H, "Terminal: whoami, ls labs, cat status.txt", body, "".join(css))


# ---------------------------------------------------------------- REPO CARDS
def card(theme, slug, kicker, title, num, unit, tags, wide):
    c = THEMES[theme]
    W, H = (1000, 170) if wide else (490, 200)
    # Small lit-dot motif in the top-right corner, echoing the portfolio background.
    dots = []
    cx, cy = W - 70, 52
    for x in range(W - 150, W - 10, 18):
        for y in range(16, 100, 18):
            d = math.hypot(x - cx, y - cy)
            if d < 60:
                k = (1 - d / 60) ** 2
                dots.append(f'<circle cx="{x}" cy="{y}" r="{1.3 + k * 1.6:.2f}" fill="{ACCENT}" fill-opacity="{0.2 + k * 0.75:.2f}"/>')
            else:
                dots.append(f'<circle cx="{x}" cy="{y}" r="1.2" fill="{c["dot"]}"/>')
    css = f"""
      .k{{font:500 14px {MONO};fill:{c['text3']}}} .flag{{fill:{c['accent_text']}}}
      .t{{font:700 {30 if wide else 26}px {SANS};letter-spacing:-0.6px;fill:{c['text']}}}
      .n{{font:700 {44 if wide else 40}px {SANS};letter-spacing:-1.5px;fill:{ACCENT}}}
      .u{{font:500 15px {SANS};fill:{c['text2']}}}
      .g{{font:400 15px {SANS};fill:{c['text2']}}}
      .hub{{transform-origin:{cx}px {cy}px;animation:pulse 2.6s ease-out infinite}}
      @keyframes pulse{{from{{transform:scale(1);opacity:.6}}to{{transform:scale(4);opacity:0}}}}
      @media (prefers-reduced-motion:reduce){{.hub{{animation:none;opacity:0}}}}
    """
    kclass = "k flag" if slug == "campus" else "k"
    if wide:
        text = (f'<text x="32" y="46" class="{kclass}">{escape(kicker)}</text>'
                f'<text x="32" y="88" class="t">{escape(title)}</text>'
                f'<text x="32" y="132" class="g">{escape(tags)}</text>'
                f'<text x="{W - 210}" y="138" class="n" text-anchor="end">{num}</text>'
                f'<text x="{W - 200}" y="138" class="u">{escape(unit)}</text>')
    else:
        text = (f'<text x="28" y="44" class="{kclass}">{escape(kicker)}</text>'
                f'<text x="28" y="86" class="t">{escape(title)}</text>'
                f'<text x="28" y="134" class="n">{num}</text>'
                f'<text x="{28 + len(num) * 24 + 8}" y="134" class="u">{escape(unit)}</text>'
                f'<text x="28" y="172" class="g">{escape(tags)}</text>')
    body = (f'<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="16" fill="{c["card"]}" stroke="{c["line"]}" stroke-width="1.5"/>'
            f'<rect x="0.75" y="0.75" width="5" height="{H - 1.5}" rx="2.5" fill="{ACCENT}"/>'
            + "".join(dots)
            + f'<circle cx="{cx}" cy="{cy}" r="6" fill="{ACCENT}"/><circle cx="{cx}" cy="{cy}" r="6" fill="none" stroke="{ACCENT}" stroke-width="1.5" class="hub"/>'
            + text)
    return svg(W, H, f"{title}: {num} {unit}. {tags}", body, css)


# ---------------------------------------------------------------- DIVIDER
def divider(theme):
    c = THEMES[theme]
    W, H, y = 1000, 28, 14
    nodes = [80, 290, 500, 710, 920]
    css = f"""
      .ln{{stroke:{c['line']};stroke-width:1.5;stroke-dasharray:5 6}}
      .nd{{fill:{c['bg']};stroke:{c['text3']};stroke-width:1.5}}
      .core{{fill:{ACCENT};stroke:none}}
      .pkt{{fill:{ACCENT};animation:move 5s linear infinite}}
      @keyframes move{{from{{transform:translateX(0)}}to{{transform:translateX({nodes[-1] - nodes[0]}px)}}}}
      @media (prefers-reduced-motion:reduce){{.pkt{{animation:none;opacity:0}}}}
    """
    body = (f'<line x1="{nodes[0]}" y1="{y}" x2="{nodes[-1]}" y2="{y}" class="ln"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{6 if i == 2 else 4.5}" class="nd{" core" if i == 2 else ""}"/>' for i, x in enumerate(nodes))
            + f'<circle cx="{nodes[0]}" cy="{y}" r="3.5" class="pkt"/>')
    return svg(W, H, "divider", body, css)


# ---------------------------------------------------------------- FOOTER (lamp, dark panel in both themes)
def footer():
    """A light bar flickers on and throws a pool of orange light downward over the heading."""
    W, H, LY = 1000, 300, 64
    cx = W / 2
    css = f"""
      .panel{{fill:#0c0c0e}}
      .pool{{transform-origin:{cx}px {LY}px;animation:open 1.3s cubic-bezier(.45,0,.55,1) .25s backwards}}
      .bar{{transform-origin:{cx}px {LY}px;animation:bar 1.3s linear .25s backwards}}
      .h{{font:700 44px {SANS};letter-spacing:-1.5px;fill:#f1f1f3}}
      .a{{fill:{ACCENT}}}
      .m{{font:400 17px {MONO};fill:#b4b4bd}}
      .txt{{animation:rise 1s ease-in-out .35s backwards}}
      @keyframes open{{from{{transform:scaleX(.4);opacity:.25}}}}
      @keyframes bar{{0%{{transform:scaleX(.4);opacity:.3}}8%{{opacity:1}}13%{{opacity:.35}}22%{{opacity:1}}28%{{opacity:.6}}38%{{opacity:1}}}}
      @keyframes rise{{from{{opacity:.35;transform:translateY(16px)}}}}
      @media (prefers-reduced-motion:reduce){{.pool,.bar,.txt{{animation:none}}}}
    """
    defs = (f'<defs>'
            f'<radialGradient id="pool" cx="{cx}" cy="{LY}" r="420" gradientUnits="userSpaceOnUse" gradientTransform="translate({cx} {LY}) scale(1 .55) translate({-cx} {-LY})">'
            f'<stop offset="0" stop-color="{ACCENT}" stop-opacity=".55"/><stop offset=".35" stop-color="{ACCENT}" stop-opacity=".2"/>'
            f'<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="barG" x1="0" x2="1"><stop offset="0" stop-color="#ffb38a" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="#fff1e8"/><stop offset="1" stop-color="#ffb38a" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="panel"><rect width="{W}" height="{H}" rx="24"/></clipPath>'
            f'<clipPath id="below"><rect x="0" y="{LY}" width="{W}" height="{H}"/></clipPath></defs>')
    body = (defs + f'<g clip-path="url(#panel)"><rect class="panel" width="{W}" height="{H}"/>'
            f'<g clip-path="url(#below)"><rect class="pool" x="0" y="{LY}" width="{W}" height="{H}" fill="url(#pool)"/></g>'
            f'<rect class="bar" x="{cx - 260}" y="{LY - 1.5}" width="520" height="3" rx="1.5" fill="url(#barG)"/>'
            f'<g class="txt"><text x="{cx}" y="{LY + 108}" text-anchor="middle" class="h">Hiring for a network or NOC role? <tspan class="a">Let\'s talk.</tspan></text>'
            f'<text x="{cx}" y="{LY + 164}" text-anchor="middle" class="m">abdulwahabsaim58.nl@gmail.com</text></g></g>')
    return svg(W, H, "Hiring for a network or NOC role? Let's talk. abdulwahabsaim58.nl@gmail.com", body, css)


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "terminal.svg").write_text(terminal())
    (OUT / "footer.svg").write_text(footer())
    for theme in THEMES:
        (OUT / f"divider-{theme}.svg").write_text(divider(theme))
        for slug, *rest in CARDS:
            (OUT / f"card-{slug}-{theme}.svg").write_text(card(theme, slug, *rest))
    print("built", sorted(p.name for p in OUT.glob("*.svg")))


if __name__ == "__main__":
    main()
