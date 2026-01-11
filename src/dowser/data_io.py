from __future__ import annotations

from pathlib import Path
import pandas as pd
import geopandas as gpd


def _find_first(root: Path, patterns: list[str]) -> Path:
    matches: list[Path] = []
    for pat in patterns:
        matches.extend(root.rglob(pat))
    if not matches:
        raise FileNotFoundError(f"Nessun file matcha {patterns} in: {root}")
    # preferisci shapefile se ci sono più opzioni
    matches = sorted(matches, key=lambda p: (p.suffix.lower() != ".shp", str(p)))
    return matches[0]


def read_adm_any(path: Path) -> gpd.GeoDataFrame:
    """
    Legge confini amministrativi da:
      - file .shp / .geojson / .gpkg
      - cartella contenente shapefile (es. tza_adm1/)
    """
    path = Path(path)
    if path.is_dir():
        f = _find_first(path, ["*.shp", "*.geojson", "*.gpkg"])
        return gpd.read_file(f)
    return gpd.read_file(path)


def read_wpdx_csv(csv_path: Path, lon_col: str = "lon", lat_col: str = "lat") -> gpd.GeoDataFrame:
    """
    Legge WPDx CSV e lo converte in GeoDataFrame (EPSG:4326).
    Autodetect per colonne coordinate comuni.
    """
    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path, low_memory=False)

    candidates = [
        ("lon_deg", "lat_deg"),
        ("lon", "lat"),
        ("longitude", "latitude"),
        ("Lon", "Lat"),
        ("LONGITUDE", "LATITUDE"),
    ]
    if lon_col not in df.columns or lat_col not in df.columns:
        for lo, la in candidates:
            if lo in df.columns and la in df.columns:
                lon_col, lat_col = lo, la
                break

    if lon_col not in df.columns or lat_col not in df.columns:
        raise ValueError(
            "Colonne coordinate non trovate. "
            f"Ho cercato {candidates}. Prime colonne: {list(df.columns)[:60]}"
        )

    # Basic sanity filter coordinate
    df = df[df[lon_col].notna() & df[lat_col].notna()].copy()
    df = df[(df[lat_col].between(-90, 90)) & (df[lon_col].between(-180, 180))]

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
        crs="EPSG:4326",
    )
    return gdf