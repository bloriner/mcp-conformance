#!/usr/bin/env python3
"""JSON report writer + local SVG score-badge generator (stdlib only).

The badge is a shields.io-style SVG generated locally — no network calls.
"""

from __future__ import annotations

import json
import os
import xml.sax.saxutils as saxutils


def write_json(report, path):
    """Write the scored report dict as pretty JSON. Returns the path."""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=False)
        fh.write("\n")
    return path


def badge_color(score):
    """shields.io-style color ramp for a 0-100 score."""
    if score >= 85:
        return "#4c1"      # brightgreen
    if score >= 70:
        return "#97ca00"  # green
    if score >= 50:
        return "#dfb317"  # yellow
    if score >= 30:
        return "#fe7d37"  # orange
    return "#e05d44"      # red


def make_badge(score, path=None, label="mcp conformance"):
    """Generate the SVG badge. Writes to ``path`` if given; returns SVG text."""
    score = int(score)
    value = "%d / 100" % score
    color = badge_color(score)
    label_esc = saxutils.escape(label)
    value_esc = saxutils.escape(value)

    # Width estimation (~6.2px per char at 11px Verdana + padding), like shields.
    label_w = int(len(label) * 6.2 + 14)
    value_w = int(len(value) * 6.2 + 14)
    total_w = label_w + value_w

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'width="{total}" height="20" role="img" aria-label="{label}: {value}">\n'
        '  <title>{label}: {value}</title>\n'
        '  <linearGradient id="s" x2="0" y2="100%">\n'
        '    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>\n'
        '    <stop offset="1" stop-opacity=".1"/>\n'
        '  </linearGradient>\n'
        '  <clipPath id="r"><rect width="{total}" height="20" rx="3" fill="#fff"/></clipPath>\n'
        '  <g clip-path="url(#r)">\n'
        '    <rect width="{lw}" height="20" fill="#555"/>\n'
        '    <rect x="{lw}" width="{vw}" height="20" fill="{color}"/>\n'
        '    <rect width="{total}" height="20" fill="url(#s)"/>\n'
        '  </g>\n'
        '  <g fill="#fff" text-anchor="middle" '
        'font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">\n'
        '    <text x="{lx}" y="15" fill="#010101" fill-opacity=".3">{label}</text>\n'
        '    <text x="{lx}" y="14">{label}</text>\n'
        '    <text x="{vx}" y="15" fill="#010101" fill-opacity=".3">{value}</text>\n'
        '    <text x="{vx}" y="14">{value}</text>\n'
        '  </g>\n'
        '</svg>\n'
    ).format(
        total=total_w, lw=label_w, vw=value_w, color=color,
        label=label_esc, value=value_esc,
        lx=(label_w + 1) // 2, vx=label_w + (value_w + 1) // 2,
    )
    if path:
        directory = os.path.dirname(os.path.abspath(path))
        os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
    return svg
