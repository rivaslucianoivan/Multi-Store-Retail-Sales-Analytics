import pandas as pd


def add_outlet_age(df: pd.DataFrame, reference_year: int = 2026) -> pd.DataFrame:
    """
    Crea la columna OutletAge a partir de EstablishmentYear.
    """
    df = df.copy()

    if "EstablishmentYear" in df.columns:
        df["OutletAge"] = reference_year - df["EstablishmentYear"]

    return df


def add_price_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Segmenta productos por nivel de precio usando MRP.
    """
    df = df.copy()

    if "MRP" in df.columns:
        df["PriceSegment"] = pd.qcut(
            df["MRP"],
            q=4,
            labels=["Low", "Medium", "High", "Premium"],
            duplicates="drop"
        )

    return df


def add_sales_share(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la participación de ventas de cada fila sobre el total.
    """
    df = df.copy()

    if "OutletSales" in df.columns:
        total_sales = df["OutletSales"].sum()
        if total_sales != 0:
            df["SalesShare"] = df["OutletSales"] / total_sales
        else:
            df["SalesShare"] = 0

    return df


def enrich_sales_data(df: pd.DataFrame, reference_year: int = 2026) -> pd.DataFrame:
    """
    Ejecuta todas las transformaciones a nivel fila.
    """
    df = add_outlet_age(df, reference_year=reference_year)
    df = add_price_segments(df)
    df = add_sales_share(df)
    return df


def build_overall_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Devuelve KPIs generales del dataset.
    """
    kpis = pd.DataFrame({
        "metric": [
            "total_sales",
            "total_products",
            "total_outlets",
            "avg_mrp",
            "avg_visibility",
            "avg_outlet_age"
        ],
        "value": [
            df["OutletSales"].sum() if "OutletSales" in df.columns else None,
            df["ProductID"].nunique() if "ProductID" in df.columns else None,
            df["OutletID"].nunique() if "OutletID" in df.columns else None,
            df["MRP"].mean() if "MRP" in df.columns else None,
            df["ProductVisibility"].mean() if "ProductVisibility" in df.columns else None,
            df["OutletAge"].mean() if "OutletAge" in df.columns else None,
        ]
    })
    return kpis


def build_outlet_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resume métricas por tienda.
    """
    summary = (
        df.groupby("OutletID", dropna=False)
        .agg(
            total_sales=("OutletSales", "sum"),
            avg_sales=("OutletSales", "mean"),
            total_products=("ProductID", "nunique"),
            avg_mrp=("MRP", "mean"),
            avg_visibility=("ProductVisibility", "mean"),
            outlet_age=("OutletAge", "mean"),
        )
        .reset_index()
        .sort_values(by="total_sales", ascending=False)
    )
    return summary


def build_product_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resume métricas por tipo de producto.
    """
    summary = (
        df.groupby("ProductType", dropna=False)
        .agg(
            total_sales=("OutletSales", "sum"),
            avg_sales=("OutletSales", "mean"),
            total_products=("ProductID", "nunique"),
            avg_mrp=("MRP", "mean"),
            avg_visibility=("ProductVisibility", "mean"),
        )
        .reset_index()
        .sort_values(by="total_sales", ascending=False)
    )
    return summary


def build_fat_content_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resume ventas y métricas por contenido graso.
    """
    summary = (
        df.groupby("FatContent", dropna=False)
        .agg(
            total_sales=("OutletSales", "sum"),
            avg_sales=("OutletSales", "mean"),
            total_products=("ProductID", "nunique"),
            avg_mrp=("MRP", "mean"),
        )
        .reset_index()
        .sort_values(by="total_sales", ascending=False)
    )
    return summary


def build_top_products(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Devuelve los productos con mayores ventas.
    """
    summary = (
        df.groupby("ProductID", dropna=False)
        .agg(
            total_sales=("OutletSales", "sum"),
            avg_mrp=("MRP", "mean"),
            outlets_selling=("OutletID", "nunique"),
        )
        .reset_index()
        .sort_values(by="total_sales", ascending=False)
        .head(top_n)
    )
    return summary


def build_outlet_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resume métricas por tipo de outlet.
    """
    summary = (
        df.groupby("OutletType", dropna=False)
        .agg(
            total_sales=("OutletSales", "sum"),
            avg_sales=("OutletSales", "mean"),
            total_outlets=("OutletID", "nunique"),
            avg_mrp=("MRP", "mean"),
        )
        .reset_index()
        .sort_values(by="total_sales", ascending=False)
    )
    return summary


def build_outlet_age_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resume métricas por antigüedad de tienda.
    """
    if "OutletAge" not in df.columns:
        raise ValueError("OutletAge column not found. Run enrich_sales_data() first.")

    summary = (
        df.groupby("OutletAge", dropna=False)
        .agg(
            total_sales=("OutletSales", "sum"),
            avg_sales=("OutletSales", "mean"),
            total_products=("ProductID", "nunique"),
            total_outlets=("OutletID", "nunique"),
        )
        .reset_index()
        .sort_values(by="OutletAge", ascending=True)
    )
    return summary


def build_price_segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resume métricas por segmento de precio.
    """
    if "PriceSegment" not in df.columns:
        raise ValueError("PriceSegment column not found. Run enrich_sales_data() first.")

    summary = (
        df.groupby("PriceSegment", dropna=False)
        .agg(
            total_sales=("OutletSales", "sum"),
            avg_sales=("OutletSales", "mean"),
            total_products=("ProductID", "nunique"),
            avg_mrp=("MRP", "mean"),
        )
        .reset_index()
    )
    return summary


def build_all_reports(df: pd.DataFrame) -> dict:
    """
    Ejecuta todas las transformaciones y devuelve todas las tablas.
    """
    df_enriched = enrich_sales_data(df)

    reports = {
        "enriched_data": df_enriched,
        "overall_kpis": build_overall_kpis(df_enriched),
        "outlet_summary": build_outlet_summary(df_enriched),
        "product_type_summary": build_product_type_summary(df_enriched),
        "fat_content_summary": build_fat_content_summary(df_enriched),
        "top_products": build_top_products(df_enriched, top_n=10),
        "outlet_type_summary": build_outlet_type_summary(df_enriched),
        "outlet_age_summary": build_outlet_age_summary(df_enriched),
        "price_segment_summary": build_price_segment_summary(df_enriched),
    }

    return reports