import pandas as pd


REQUIRED_COLUMNS = [
    "ProductID",
    "Weight",
    "FatContent",
    "ProductVisibility",
    "ProductType",
    "MRP",
    "OutletID",
    "EstablishmentYear",
    "OutletSize",
    "LocationType",
    "OutletType",
    "OutletSales",
]

TEXT_COLUMNS = [
    "ProductID",
    "FatContent",
    "ProductType",
    "OutletID",
    "OutletSize",
    "LocationType",
    "OutletType",
]

NUMERIC_COLUMNS = [
    "Weight",
    "ProductVisibility",
    "MRP",
    "OutletSales",
]

INTEGER_COLUMNS = [
    "EstablishmentYear",
]

DUPLICATE_SUBSET = [
    "ProductID",
    "OutletID",
    "MRP",
    "OutletSales",
]


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Asegura que las columnas queden con los nombres canónicos del proyecto.
    """
    df = df.copy()

    rename_map = {
        "item_identifier": "ProductID",
        "item_weight": "Weight",
        "item_fat_content": "FatContent",
        "item_visibility": "ProductVisibility",
        "productvisibility": "ProductVisibility",
        "item_type": "ProductType",
        "item_mrp": "MRP",
        "outlet_identifier": "OutletID",
        "establishmentyear": "EstablishmentYear",
        "outlet_establishment_year": "EstablishmentYear",
        "outlet_size": "OutletSize",
        "outlet_location_type": "LocationType",
        "location_type": "LocationType",
        "outlet_type": "OutletType",
        "item_outlet_sales": "OutletSales",
    }

    cleaned_cols = {}
    for col in df.columns:
        key = str(col).strip()
        normalized = key.lower().replace(" ", "_")
        cleaned_cols[col] = rename_map.get(normalized, key)

    df = df.rename(columns=cleaned_cols)
    return df


def validate_required_columns(df: pd.DataFrame) -> None:
    """
    Verifica que estén todas las columnas esperadas.
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def normalize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia espacios y estandariza categorías de texto.
    """
    df = df.copy()

    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    if "FatContent" in df.columns:
        df["FatContent"] = df["FatContent"].replace({
            "LF": "Low Fat",
            "low fat": "Low Fat",
            "Low fat": "Low Fat",
            "reg": "Regular",
            "regular": "Regular",
        })

    return df


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte columnas a tipos correctos.
    """
    df = df.copy()

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "EstablishmentYear" in df.columns:
        df["EstablishmentYear"] = pd.to_numeric(
            df["EstablishmentYear"], errors="coerce"
        ).astype("Int64")

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata valores faltantes con reglas simples y consistentes.
    """
    df = df.copy()

    if "Weight" in df.columns and "ProductID" in df.columns:
        weight_by_product = df.groupby("ProductID")["Weight"].transform("median")
        df["Weight"] = df["Weight"].fillna(weight_by_product)

    if "OutletSize" in df.columns:
        mode_outlet_size = df["OutletSize"].mode(dropna=True)
        if not mode_outlet_size.empty:
            df["OutletSize"] = df["OutletSize"].fillna(mode_outlet_size.iloc[0])

    return df


def remove_duplicates(
    df: pd.DataFrame,
    subset: list | None = None
) -> pd.DataFrame:
    """
    Elimina duplicados exactos o lógicos.
    """
    df = df.copy()
    dup_subset = subset if subset is not None else DUPLICATE_SUBSET
    dup_subset = [col for col in dup_subset if col in df.columns]

    if dup_subset:
        df = df.drop_duplicates(subset=dup_subset)
    else:
        df = df.drop_duplicates()

    return df


def filter_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas con valores imposibles o no útiles para análisis.
    """
    df = df.copy()

    if "MRP" in df.columns:
        df = df[df["MRP"] > 0]

    if "OutletSales" in df.columns:
        df = df[df["OutletSales"] >= 0]

    if "ProductVisibility" in df.columns:
        df = df[df["ProductVisibility"] >= 0]

    if "EstablishmentYear" in df.columns:
        df = df[
            df["EstablishmentYear"].between(1900, 2030, inclusive="both")
            | df["EstablishmentYear"].isna()
        ]

    if "OutletID" in df.columns:
        df = df[df["OutletID"].notna()]

    if "ProductID" in df.columns:
        df = df[df["ProductID"].notna()]

    return df


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ejecuta el pipeline completo de limpieza.
    """
    df = standardize_column_names(df)
    validate_required_columns(df)
    df = normalize_text_columns(df)
    df = convert_data_types(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = filter_invalid_rows(df)
    return df


def build_data_quality_report(
    df_before: pd.DataFrame,
    df_after: pd.DataFrame
) -> pd.DataFrame:
    """
    Resume el impacto de la limpieza.
    """
    report = pd.DataFrame({
        "metric": [
            "rows_before",
            "rows_after",
            "rows_removed",
            "columns_before",
            "columns_after",
            "nulls_before",
            "nulls_after",
            "duplicates_before",
            "duplicates_after",
        ],
        "value": [
            len(df_before),
            len(df_after),
            len(df_before) - len(df_after),
            df_before.shape[1],
            df_after.shape[1],
            int(df_before.isna().sum().sum()),
            int(df_after.isna().sum().sum()),
            int(df_before.duplicated().sum()),
            int(df_after.duplicated().sum()),
        ]
    })
    return report