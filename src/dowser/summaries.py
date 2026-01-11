from __future__ import annotations
import pandas as pd


def quality_report(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    out.append(("n_rows", len(df)))
    for c in ["lat", "lon", "latitude", "longitude"]:
        if c in df.columns:
            out.append((f"missing_{c}", int(df[c].isna().sum())))
    for c in ["country_name", "adm1", "adm2", "status", "water_source", "technology", "management"]:
        if c in df.columns:
            out.append((f"n_unique_{c}", int(df[c].nunique(dropna=True))))
    return pd.DataFrame(out, columns=["metric", "value"])


def admin_counts(df: pd.DataFrame, admin_col: str) -> pd.DataFrame:
    if admin_col not in df.columns:
        raise ValueError(f"Colonna {admin_col} non trovata. Colonne: {list(df.columns)[:80]}")
    return (
        df.groupby(admin_col, dropna=False)
        .size()
        .reset_index(name="n_points")
        .sort_values("n_points", ascending=False)
    )