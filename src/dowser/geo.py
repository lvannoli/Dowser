from __future__ import annotations
import geopandas as gpd


def normalize_crs(points: gpd.GeoDataFrame, polygons: gpd.GeoDataFrame) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """
    Porta entrambi nello stesso CRS.
    Se polygons.crs è None, assume EPSG:4326 (ultimo resort).
    """
    if polygons.crs is None:
        polygons = polygons.set_crs("EPSG:4326")
    if points.crs is None:
        points = points.set_crs("EPSG:4326")

    points = points.to_crs(polygons.crs)
    return points, polygons


def spatial_join_points(points: gpd.GeoDataFrame, polygons: gpd.GeoDataFrame, keep_poly_cols: list[str]) -> gpd.GeoDataFrame:
    """
    Spatial join (within): ogni punto eredita attributi dal poligono che lo contiene.
    """
    p, poly = normalize_crs(points, polygons)

    # riduci poligoni alle sole colonne utili
    cols = [c for c in keep_poly_cols if c in poly.columns]
    poly = poly[cols + ["geometry"]].copy()

    joined = gpd.sjoin(p, poly, how="left", predicate="within")
    if "index_right" in joined.columns:
        joined = joined.drop(columns=["index_right"])
    return joined