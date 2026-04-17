"""
analysis.py — Data analysis engine for Life Dashboard.

This module is PURELY FUNCTIONAL — no database access, no side effects.
It takes a list of data dictionaries and returns computed statistics.

Uses:
  - pandas for data manipulation and averages
  - scipy.stats for Pearson correlation coefficients
"""

import pandas as pd
from scipy.stats import pearsonr
from typing import Any


def compute_stats(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Compute all statistics from the user's life data.

    Args:
        entries: A list of dicts, each with keys:
                 study_hours, sleep_hours, screen_time, mood, date

    Returns:
        A dict containing:
          - averages (sleep, study, screen_time, mood)
          - correlations (sleep↔mood, sleep↔study, screen_time↔mood)
          - best_day / worst_day (date + mood)
          - mood_trend ("improving", "declining", or "stable")
          - entry_count
    """

    df = pd.DataFrame(entries)

    # --- Averages ---
    averages = {
        "avg_sleep_hours": round(df["sleep_hours"].mean(), 2),
        "avg_study_hours": round(df["study_hours"].mean(), 2),
        "avg_screen_time": round(df["screen_time"].mean(), 2),
        "avg_mood": round(df["mood"].mean(), 2),
    }

    # --- Pearson Correlations ---
    # pearsonr returns (correlation_coefficient, p_value)
    # We only need the coefficient; handle cases where std dev is 0
    correlations = {}

    correlation_pairs = [
        ("sleep_vs_mood", "sleep_hours", "mood"),
        ("sleep_vs_study", "sleep_hours", "study_hours"),
        ("screen_time_vs_mood", "screen_time", "mood"),
    ]

    for label, col_a, col_b in correlation_pairs:
        # Need at least 2 data points and non-zero variance for correlation
        if len(df) >= 2 and df[col_a].std() > 0 and df[col_b].std() > 0:
            corr, _ = pearsonr(df[col_a], df[col_b])
            correlations[label] = round(corr, 3)
        else:
            correlations[label] = None  # Not enough data to compute

    # --- Best & Worst Day ---
    best_idx = df["mood"].idxmax()
    worst_idx = df["mood"].idxmin()

    best_day = {
        "date": str(df.loc[best_idx, "date"]),
        "mood": int(df.loc[best_idx, "mood"]),
    }
    worst_day = {
        "date": str(df.loc[worst_idx, "date"]),
        "mood": int(df.loc[worst_idx, "mood"]),
    }

    # --- Mood Trend (last 7 entries) ---
    mood_trend = _compute_mood_trend(df)

    return {
        "entry_count": len(df),
        "averages": averages,
        "correlations": correlations,
        "best_day": best_day,
        "worst_day": worst_day,
        "mood_trend": mood_trend,
    }


def _compute_mood_trend(df: pd.DataFrame) -> str:
    """
    Determine whether mood is improving, declining, or stable
    over the last 7 entries (sorted by date).

    Uses simple linear comparison: average of first half vs second half.
    """

    # Sort by date and take last 7
    recent = df.sort_values("date").tail(7)

    if len(recent) < 3:
        return "not enough data"

    midpoint = len(recent) // 2
    first_half_avg = recent["mood"].iloc[:midpoint].mean()
    second_half_avg = recent["mood"].iloc[midpoint:].mean()

    diff = second_half_avg - first_half_avg

    if diff > 0.5:
        return "improving"
    elif diff < -0.5:
        return "declining"
    else:
        return "stable"
