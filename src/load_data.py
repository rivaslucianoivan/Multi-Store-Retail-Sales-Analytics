from pathlib import Path
from typing import List
import pandas as pd

# Rutas y patrones por defecto
RAW_STORES_DIR = Path("./data/raw/stores")
DEFAULT_STORE_PATTERN = "*.csv"
STORE_ID_COL = "OutletID"


def get_store_files(
    raw_dir: Path = RAW_STORES_DIR,
    pattern: str = DEFAULT_STORE_PATTERN
) -> List[Path]:
    raw_dir = Path(raw_dir)
    files = sorted(raw_dir.glob(pattern))
    return files


def extract_store_id_from_filename(path: Path) -> str:
    stem = path.stem  # nombre sin extensión
    # Tomar la última parte separada por '_'
    parts = stem.split("_")
    store_id = parts[-1]
    return store_id


def load_store_file(
    path: Path,
    add_store_id_if_missing: bool = True,
    store_id_col: str = STORE_ID_COL
) -> pd.DataFrame:
    path = Path(path)
    df = pd.read_csv(path)

    # Si no viene la columna Outlet_Identifier, la infiere del nombre del archivo
    if add_store_id_if_missing and store_id_col not in df.columns:
        df[store_id_col] = extract_store_id_from_filename(path)

    # Columna útil para trazabilidad
    df["source_file"] = path.name

    return df


def load_all_stores(
    raw_dir: Path = RAW_STORES_DIR,
    pattern: str = DEFAULT_STORE_PATTERN,
    store_id_col: str = STORE_ID_COL
) -> pd.DataFrame:
    files = get_store_files(raw_dir=raw_dir, pattern=pattern)

    if not files:
        raise FileNotFoundError(
            f"No store files found in {raw_dir} with pattern '{pattern}'"
        )

    dfs = []
    for f in files:
        df_store = load_store_file(f, add_store_id_if_missing=True, store_id_col=store_id_col)
        dfs.append(df_store)

    combined = pd.concat(dfs, ignore_index=True)

    return combined


def quick_preview(df: pd.DataFrame, n: int = 5) -> None:
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(df.head(n))