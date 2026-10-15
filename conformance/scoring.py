#!/usr/bin/env python3
"""Scoring for the MCP conformance suite (stdlib only).

Each check has a weight inside its category; a category subscore is the
weight-weighted pass fraction (0-100). The total score is the weighted sum
of the category subscores, rounded to an integer 0-100.
"""

from __future__ import annotations

CATEGORY_WEIGHTS = {
    "protocol": 0.40,   # handshake, tool shapes, JSON-RPC error codes, notifications
    "safety": 0.35,     # leak probing, oversized input, injection resistance
    "quality": 0.25,    # latency, schema validity
}


def score_suite(suite_result):
    """Attach scores to a runner.run_suite() result dict. Returns a new dict."""
    checks = suite_result.get("checks", [])
    categories = {}
    for category, cat_weight in CATEGORY_WEIGHTS.items():
        cat_checks = [c for c in checks if c.get("category") == category]
        total_w = sum(c.get("weight", 0) for c in cat_checks)
        passed_w = sum(c.get("weight", 0) for c in cat_checks if c.get("passed"))
        sub = 100.0 * passed_w / total_w if total_w else 0.0
        categories[category] = {
            "score": round(sub, 1),
            "weight": cat_weight,
            "passed": sum(1 for c in cat_checks if c.get("passed")),
            "total": len(cat_checks),
        }
    total = sum(categories[c]["score"] * w for c, w in CATEGORY_WEIGHTS.items())
    report = dict(suite_result)
    report["categories"] = categories
    report["score"] = max(0, min(100, int(round(total))))
    report["passed"] = sum(1 for c in checks if c.get("passed"))
    report["check_count"] = len(checks)
    return report


def grade(score):
    """Letter-ish grade for a 0-100 score."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 50:
        return "D"
    return "F"
