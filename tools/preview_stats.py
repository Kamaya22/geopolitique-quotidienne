#!/usr/bin/env python3
"""Génère un aperçu HTML autonome des statistiques de sources (barres colorées,
spectre politique gauche→droite, camemberts SVG). Réutilise exactement le calcul
de build_stats.py. Aperçu local uniquement — pas utilisé par le pipeline.

Usage : python tools/preview_stats.py [--open]
"""

import math
import os
import sys
import webbrowser
from html import escape

from build_stats import (REPO_ROOT, alertes_list, compute_stats, load_citations,
                         load_registry, pct)

OUT = os.path.join(REPO_ROOT, "stats-preview.html")

# Spectre politique gauche → droite + familles neutres. Ordre = position sur l'axe.
ORDER = ["extreme-gauche", "gauche", "centre-gauche", "centre", "centre-droit",
         "droite", "droite-souverainiste", "liberal", "droite-liberale",
         "independant", "factuel", "a-verifier", "(hors registre)"]
COLORS = {
    "extreme-gauche": "#a11", "gauche": "#e63946", "centre-gauche": "#f4978e",
    "centre": "#6c757d", "centre-droit": "#9ec5e8", "droite": "#1d6fb8",
    "droite-souverainiste": "#0b3d66", "liberal": "#3aa0a0",
    "droite-liberale": "#4c7fb0", "independant": "#6f42c1", "factuel": "#adb5bd",
    "a-verifier": "#ffc107", "(hors registre)": "#dc3545",
}
PALETTE = ["#1d6fb8", "#e63946", "#2a9d8f", "#6f42c1", "#f4a261", "#6c757d",
           "#0b3d66", "#9ec5e8", "#e76f51", "#adb5bd", "#3aa0a0", "#264653"]


def color_for(value, i=0):
    return COLORS.get(value, PALETTE[i % len(PALETTE)])


def bars(counter, total, color_by_value=False, order=None):
    items = list(counter.most_common())
    if order:
        items.sort(key=lambda kv: order.index(kv[0]) if kv[0] in order else 999)
    mx = max((n for _, n in items), default=1)
    rows = []
    for i, (value, n) in enumerate(items):
        p = pct(n, total)
        w = 100.0 * n / mx
        col = color_for(value, i) if color_by_value else PALETTE[i % len(PALETTE)]
        rows.append(
            f'<div class="row"><div class="lbl">{escape(str(value) or "—")}</div>'
            f'<div class="track"><div class="bar" style="width:{w:.1f}%;background:{col}"></div></div>'
            f'<div class="val">{n} · {p:.1f} %</div></div>'
        )
    return "\n".join(rows)


def donut(counter, total, color_by_value=False):
    """Camembert SVG (donut) simple."""
    items = list(counter.most_common())
    r, cx, cy, sw = 60, 80, 80, 34
    circ = 2 * math.pi * r
    offset = 0.0
    segs, legend = [], []
    for i, (value, n) in enumerate(items):
        frac = (n / total) if total else 0
        col = color_for(value, i) if color_by_value else PALETTE[i % len(PALETTE)]
        dash = frac * circ
        segs.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" '
            f'stroke-width="{sw}" stroke-dasharray="{dash:.2f} {circ - dash:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 {cx} {cy})"/>'
        )
        offset += dash
        legend.append(
            f'<div class="leg"><span class="dot" style="background:{col}"></span>'
            f'{escape(str(value) or "—")} — {pct(n, total):.1f} %</div>'
        )
    svg = f'<svg width="160" height="160" viewBox="0 0 160 160">{"".join(segs)}</svg>'
    return f'<div class="donutwrap">{svg}<div class="legend">{"".join(legend)}</div></div>'


def card(title, body, note=""):
    note = f'<p class="note">{note}</p>' if note else ""
    return f'<section class="card"><h2>{escape(title)}</h2>{note}{body}</section>'


def main():
    s = compute_stats(load_registry(), load_citations())
    total = s["total"]

    summary = "".join(
        f'<div class="kpi"><div class="num">{v}</div><div class="cap">{escape(k)}</div></div>'
        for k, v in [
            ("citations", total),
            ("éditions", s["n_editions"]),
            ("sources distinctes", len({sid for (sid, _) in s["par_source"]})),
            ("pays", len(s["par_pays"])),
            ("orientations", len(s["par_orientation"])),
        ]
    )

    al = alertes_list(s)
    if al:
        alerts_html = '<ul class="alerts">' + "".join(f"<li>{escape(a)}</li>" for a in al) + "</ul>"
    else:
        alerts_html = '<p class="ok">✓ Aucune alerte : pas de hors-registre, pas d\'orientation à vérifier, pas de concentration au-delà des seuils.</p>'

    top = "".join(
        f'<div class="row"><div class="lbl">{escape(nom)}</div>'
        f'<div class="track"><div class="bar" style="width:{100.0*n/max(1,s["par_source"].most_common(1)[0][1]):.1f}%;background:#264653"></div></div>'
        f'<div class="val">{n}</div></div>'
        for (sid, nom), n in s["par_source"].most_common(15)
    )

    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>Aperçu des statistiques de sources</title>
<style>
:root{{font-family:-apple-system,Segoe UI,Roboto,sans-serif}}
body{{margin:0;background:#f4f5f7;color:#1a1a1a;padding:24px}}
h1{{margin:0 0 4px}} .sub{{color:#666;margin:0 0 20px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:16px}}
.card{{background:#fff;border-radius:12px;padding:18px 20px;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
.card h2{{font-size:15px;margin:0 0 14px;text-transform:uppercase;letter-spacing:.04em;color:#333}}
.kpis{{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:16px}}
.kpi{{background:#fff;border-radius:12px;padding:14px 20px;box-shadow:0 1px 3px rgba(0,0,0,.08);min-width:110px;text-align:center}}
.kpi .num{{font-size:30px;font-weight:700;color:#1d6fb8}} .kpi .cap{{font-size:12px;color:#666}}
.row{{display:grid;grid-template-columns:150px 1fr auto;align-items:center;gap:10px;margin:6px 0;font-size:13px}}
.lbl{{text-align:right;color:#333;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.track{{background:#eef0f2;border-radius:6px;height:18px;overflow:hidden}}
.bar{{height:100%;border-radius:6px}} .val{{color:#555;white-space:nowrap;font-variant-numeric:tabular-nums}}
.donutwrap{{display:flex;gap:16px;align-items:center;flex-wrap:wrap}}
.legend{{font-size:12px}} .leg{{margin:3px 0}} .dot{{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px}}
.alerts{{margin:0;padding-left:18px;color:#9a6700}} .alerts li{{margin:4px 0}}
.ok{{color:#1a7f37;margin:0}} .note{{font-size:12px;color:#888;margin:-6px 0 12px}}
.full{{grid-column:1/-1}}
</style></head><body>
<h1>Aperçu des statistiques de sources</h1>
<p class="sub">Période {escape(s['periode'])} · aperçu local généré par <code>tools/preview_stats.py</code> (mêmes chiffres que STATS.md)</p>
<div class="kpis">{summary}</div>
<div class="grid">
{card("Alertes & qualité", alerts_html)}
{card("Orientation politique", donut(s["par_orientation"], total, color_by_value=True), "Couleurs : rouge = gauche, bleu = droite, gris = factuel, violet = indépendant, ambre = à vérifier.")}
{card("Spectre politique (gauche → droite)", bars(s["par_orientation"], total, color_by_value=True, order=ORDER))}
{card("Pays d'origine", bars(s["par_pays"], total))}
{card("Type de source", donut(s["par_type"], total))}
{card("Sujet France / Monde", bars(s["par_sujet"], total))}
{card("Rôle (fait / analyse / opinion)", bars(s["par_role"], total))}
{card("Emplacement (lien formel / mention)", bars(s["par_emplacement"], total))}
{card("Sources les plus citées (top 15)", top)}
</div></body></html>"""

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Apercu HTML genere -> {OUT}")
    if "--open" in sys.argv:
        webbrowser.open("file://" + OUT.replace("\\", "/"))


if __name__ == "__main__":
    main()
