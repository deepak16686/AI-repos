"""Shared helpers for generating the triage diagrams (diagram tooling only)."""
import html
import os
import json
import re

PKG = os.environ.get("SIMPLE_ICONS_DIR", "./simple-icons/package")
_meta = json.load(open(f"{PKG}/_data/simple-icons.json"))
_meta = _meta["icons"] if isinstance(_meta, dict) else _meta
_hex = {m["title"]: m["hex"] for m in _meta}
warnings = []


def brand(slug):
    svg = open(f"{PKG}/icons/{slug}.svg", encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", svg).group(1)
    d = re.search(r' d="([^"]+)"', svg).group(1)
    return {"kind": "brand", "d": d, "hex": _hex.get(title, "334155")}


def glyph(name):
    return {"kind": "glyph", "name": name}


GLYPHS = {
    "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M14 9l2 2"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "webhook": '<path d="M3 12h11M10 7l5 5-5 5M19 5v14"/>',
    "loop": '<path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5"/>',
    "switch": '<rect x="2" y="8" width="20" height="8" rx="4"/><circle cx="16" cy="12" r="2.5" fill="currentColor"/>',
    "list": '<path d="M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
    "db": '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "plug": '<path d="M9 3v5M15 3v5M6 8h12v4a6 6 0 0 1-12 0zM12 18v3"/>',
    "gate": '<rect x="4" y="10" width="16" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "branch": '<circle cx="6" cy="5" r="2.2"/><circle cx="6" cy="19" r="2.2"/><circle cx="18" cy="9" r="2.2"/><path d="M6 7.2v9.6M18 11.2c0 4-6 3-12 6"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l3 3 5-6"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.3"/>',
    "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
    "flask": '<path d="M9 3h6M10 3v6L4 19a2 2 0 0 0 2 3h12a2 2 0 0 0 2-3l-6-10V3"/>',
    "rocket": '<path d="M5 15c-1 1-2 4-2 6 2 0 5-1 6-2M14 4c3-1 6-1 7-1 0 1 0 4-1 7l-7 7-6-6zM9 9l6 6"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 21h4"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
    "cloud": '<path d="M7 18a4 4 0 0 1-.5-8 6 6 0 0 1 11.5 1.5A3.5 3.5 0 0 1 17.5 18z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "stop": '<circle cx="12" cy="12" r="9"/><path d="M8 8l8 8M16 8l-8 8"/>',
}

I = {n: brand(s) for n, s in {
    "gitlab": "gitlab", "docker": "docker", "ollama": "ollama", "nvidia": "nvidia", "openai": "openai",
    "claude": "claude", "redis": "redis", "postgres": "postgresql", "grafana": "grafana",
    "prometheus": "prometheus", "jaeger": "jaeger", "sonar": "sonarqube", "sonatype": "sonatype",
    "vault": "vault", "trivy": "trivy", "yaml": "yaml", "python": "python", "minio": "minio",
    "git": "git", "fastapi": "fastapi", "opentelemetry": "opentelemetry"}.items()}

TEXT = {"n": "#374151", "b": "#111827", "g": "#15803d", "a": "#b45309", "r": "#b91c1c", "m": "#64748b"}


def esc(s):
    return html.escape(s, quote=False)


def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def icon_svg(ic, cx, cy, size):
    s = size / 24.0
    tx, ty = cx - size / 2, cy - size / 2
    if ic["kind"] == "brand":
        col = "#" + ic["hex"]
        if lum(ic["hex"]) > 0.7:
            col = "#111827"
        return f'<path transform="translate({tx:.1f},{ty:.1f}) scale({s:.3f})" d="{ic["d"]}" fill="{col}"/>'
    return (f'<g transform="translate({tx:.1f},{ty:.1f}) scale({s:.3f})" fill="none" stroke="#334155" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" color="#334155">{GLYPHS[ic["name"]]}</g>')


def tile(x, y, icons, size=44):
    if not isinstance(icons, list):
        icons = [icons]
    n = len(icons)
    h = size if n == 1 else n * 22 + 10
    first = icons[0]
    light = first["kind"] == "brand" and lum(first["hex"]) > 0.7 and n == 1
    fill = "#" + first["hex"] if light else "#f1f5f9"
    out = [f'<rect x="{x}" y="{y}" width="{size}" height="{h}" rx="10" fill="{fill}" stroke="#e2e8f0"/>']
    if n == 1:
        out.append(icon_svg(first, x + size / 2, y + h / 2, size * 0.58))
    else:
        for i, ic in enumerate(icons):
            out.append(icon_svg(ic, x + size / 2, y + 17 + i * 22, 17))
    return "".join(out)


def card(x, y, w, h, icons, title, lines, stroke="#cbd5e1", fill="#ffffff", dashed=False, sw=1.5, tsize=44):
    out = []
    dash = ' stroke-dasharray="6 3"' if dashed else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')
    out.append(tile(x + 10, y + (10 if h > 60 else (h - tsize) / 2), icons, tsize))
    tx = x + 10 + tsize + 12
    avail = w - (tx - x) - 8
    ty = y + 24 if h > 60 else y + h / 2 - 4
    if len(title) * 7.4 > avail:
        warnings.append(f"TITLE too long: {title!r} ({len(title) * 7.4:.0f}>{avail})")
    out.append(f'<text x="{tx}" y="{ty}" font-size="13" font-weight="700" fill="{TEXT["b"]}">{esc(title)}</text>')
    for i, ln in enumerate(lines):
        style, txt = ln if isinstance(ln, tuple) else ("n", ln)
        if len(txt) * 5.9 > avail:
            warnings.append(f"LINE too long: {txt!r} ({len(txt) * 5.9:.0f}>{avail})")
        weight = ' font-weight="700"' if style == "b" else ""
        col = TEXT["n"] if style == "b" else TEXT[style]
        out.append(f'<text x="{tx}" y="{ty + 18 + i * 15.5:.1f}" font-size="11" fill="{col}"{weight}>{esc(txt)}</text>')
    return "".join(out)


def region(x, y, w, h, title, icon, stroke, fill, tcol, dashed=False):
    dash = ' stroke-dasharray="8 4"' if dashed else ""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"{dash}/>']
    if icon is not None:
        out.append(icon_svg(icon, x + 26, y + 22, 24))
        out.append(f'<text x="{x + 48}" y="{y + 28}" font-size="15" font-weight="700" fill="{tcol}">{esc(title)}</text>')
    else:
        out.append(f'<text x="{x + 16}" y="{y + 28}" font-size="15" font-weight="700" fill="{tcol}">{esc(title)}</text>')
    return "".join(out)


def badge(cx, cy, n):
    r = 11 if str(n).isdigit() and int(n) >= 10 else 10
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#111827" stroke="#fff" stroke-width="1.5"/>'
            f'<text x="{cx}" y="{cy + 3.5}" font-size="10" font-weight="700" fill="#fff" text-anchor="middle">{n}</text>')


def t(x, y, s, size=11, fill="#374151", anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'


def svg_doc(W, H, title, body, desc=""):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Arial, Helvetica, sans-serif">
<title>{esc(title)}</title>
<defs>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#475569"/></marker>
<style>
.ar{{stroke:#475569;stroke-width:1.8;fill:none;marker-end:url(#arr)}}
.ar2{{stroke:#475569;stroke-width:1.8;fill:none;marker-end:url(#arr);marker-start:url(#arr)}}
.ds{{stroke:#64748b;stroke-width:1.6;fill:none;stroke-dasharray:6 4;marker-end:url(#arr)}}
.halo{{paint-order:stroke;stroke:#ffffff;stroke-width:3.5px;stroke-linejoin:round}}
</style>
</defs>
<rect width="{W}" height="{H}" fill="#ffffff"/>
{body}
</svg>
'''


# ---------------------------------------------------------------- sequence diagrams
def sequence(W, cols, rows, title, subtitle, left=110):
    """cols: list of (label, sub, icon). rows: tuples, see below."""
    n = len(cols)
    sp = (W - 2 * left) / (n - 1)
    xs = [left + i * sp for i in range(n)]
    head_y = 74
    y = head_y + 120
    draw, frames, counter = [], [], 0
    open_frames = []
    for row in rows:
        k = row[0]
        if k == "phase":
            draw.append(f'<rect x="16" y="{y - 14}" width="{W - 32}" height="26" rx="6" fill="#eef2ff" stroke="#c7d2fe"/>')
            draw.append(t(28, y + 4, row[1], 12, "#3730a3", extra='font-weight="700"'))
            y += 38
        elif k == "msg":
            _, a, b, text, dashed = row
            counter += 1
            label = f"{counter}. {text}"
            dist = abs(xs[b] - xs[a])
            if len(label) * 5.9 > dist - 12:
                warnings.append(f"SEQ text too long ({len(label) * 5.9:.0f}>{dist - 12:.0f}): {label!r}")
            cls = "ds" if dashed else "ar"
            x1 = xs[a] + (3 if b > a else -3)
            x2 = xs[b] + (-3 if b > a else 3)
            draw.append(f'<path d="M{x1:.1f},{y} L{x2:.1f},{y}" class="{cls}"/>')
            draw.append(t((xs[a] + xs[b]) / 2, y - 6, label, 11, "#1f2937", "middle", 'class="halo"'))
            y += 32
        elif k == "self":
            _, a, text = row
            counter += 1
            label = f"{counter}. {text}"
            x = xs[a]
            draw.append(f'<path d="M{x + 2:.1f},{y - 4} L{x + 38:.1f},{y - 4} L{x + 38:.1f},{y + 14} L{x + 4:.1f},{y + 14}" class="ar"/>')
            draw.append(t(x + 46, y + 8, label, 11, "#1f2937", extra='class="halo"'))
            y += 36
        elif k == "note":
            _, a, b, lines, color = row
            x1, x2 = xs[a] - 84, xs[b] + 84
            h = 14 * len(lines) + 12
            fills = {"y": ("#fef9c3", "#ca8a04"), "r": ("#fee2e2", "#ef4444"), "g": ("#dcfce7", "#16a34a"), "b": ("#dbeafe", "#3b82f6")}
            f, s = fills[color]
            draw.append(f'<rect x="{x1:.1f}" y="{y - 6}" width="{x2 - x1:.1f}" height="{h}" rx="6" fill="{f}" stroke="{s}"/>')
            for i, ln in enumerate(lines):
                if len(ln) * 5.9 > (x2 - x1) - 16:
                    warnings.append(f"NOTE too long: {ln!r}")
                draw.append(t(x1 + 8, y + 9 + i * 14, ln, 11, "#1f2937"))
            y += h + 12
        elif k == "frame_start":
            _, label, a, b = row
            open_frames.append([label, a, b, y - 18])
            y += 30
        elif k == "frame_end":
            label, a, b, y0 = open_frames.pop()
            frames.append((label, a, b, y0, y - 8))
            y += 8
    y_end = y + 10
    pre = []
    for i, (label, sub, icon) in enumerate(cols):
        x = xs[i]
        pre.append(f'<path d="M{x:.1f},{head_y + 70} L{x:.1f},{y_end}" stroke="#94a3b8" stroke-width="1.3" stroke-dasharray="5 4" fill="none"/>')
        pre.append(tile(round(x - 22), head_y, icon, 44))
        pre.append(t(x, head_y + 62, label, 12, "#111827", "middle", 'font-weight="700"'))
        pre.append(t(x, head_y + 78, sub, 10, "#64748b", "middle"))
    fr = []
    for label, a, b, y0, y1 in frames:
        x1, x2 = xs[a] - 70, xs[b] + 70
        fr.append(f'<rect x="{x1:.1f}" y="{y0}" width="{x2 - x1:.1f}" height="{y1 - y0}" rx="6" fill="none" stroke="#6366f1" stroke-width="1.5" stroke-dasharray="7 4"/>')
        fr.append(f'<rect x="{x1:.1f}" y="{y0}" width="{len(label) * 6.3 + 16:.0f}" height="18" rx="4" fill="#6366f1"/>')
        fr.append(t(x1 + 8, y0 + 13, label, 11, "#ffffff", extra='font-weight="700"'))
    H = int(y_end + 40)
    body = [t(30, 30, title, 22, "#111827", extra='font-weight="700"'), t(30, 52, subtitle, 12, "#475569")] + pre + fr + draw
    return W, H, "\n".join(body)
