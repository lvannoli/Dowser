from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"

RAW_BOUNDARIES = RAW / "boundaries"
RAW_WPDX = RAW / "wpdx"

INTERIM_BOUNDARIES = INTERIM / "boundaries"
INTERIM_POINTS = INTERIM / "points"

INTERIM_POINTS_TZA = INTERIM_POINTS / "tza"
INTERIM_POINTS_KEN = INTERIM_POINTS / "ken"

PROCESSED_DATASETS = PROCESSED / "datasets"

OUTPUTS = ROOT / "outputs"
TABLES = OUTPUTS / "tables"
LOGS = OUTPUTS / "logs"
FIGURES = OUTPUTS / "figures"

for p in [
    INTERIM_BOUNDARIES,
    INTERIM_POINTS_TZA,
    INTERIM_POINTS_KEN,
    PROCESSED_DATASETS,
    TABLES,
    LOGS,
    FIGURES,
]:
    p.mkdir(parents=True, exist_ok=True)
