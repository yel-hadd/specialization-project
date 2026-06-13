"""Shared helpers for the analytics layer."""

import re

import pandas as pd


def natural_period_key(period) -> tuple:
    """Sort key so period labels order naturally (S1 < S2 < S10, Trimestre 1 < 2)."""
    s = str(period)
    m = re.search(r"\d+", s)
    if m:
        return (0, int(m.group()), s)
    return (1, 0, s)


def ordered_periods(g: pd.DataFrame) -> list[str]:
    """Return the distinct periods in ``g`` in the right order.

    Chronological by the earliest date when every period carries a date,
    otherwise by natural label order (so "S10" comes after "S2", not after "S1").
    """
    if "period" not in g.columns:
        return []
    sub = g.dropna(subset=["period"])
    if sub.empty:
        return []
    periods = [str(p) for p in sub["period"].unique()]
    if "date" in sub.columns:
        mins = sub.dropna(subset=["date"]).groupby("period")["date"].min()
        if len(mins) == len(periods):  # every period has at least one date
            return [str(p) for p in mins.sort_values().index]
    return sorted(periods, key=natural_period_key)
