from pathlib import Path
from datetime import datetime
from typing import Dict

import pandas as pd


DEFAULT_REPORTS_DIR = Path("reports/final")


def build_report_filepath(
    reports_dir: Path = DEFAULT_REPORTS_DIR,
    prefix: str = "retail_sales_report",
    extension: str = ".xlsx",
) -> Path:
    """
    Construye un nombre de archivo con fecha, por ejemplo:
    reports/final/retail_sales_report_2026-04-10.xlsx
    """
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{prefix}_{date_str}{extension}"
    return reports_dir / filename


def write_df_with_format(
    writer: pd.ExcelWriter,
    df: pd.DataFrame,
    sheet_name: str,
    index: bool = False,
    float_format: str = "0.00",
) -> None:
    """
    Escribe un DataFrame en una hoja de Excel y aplica formato básico
    (números con 2 decimales y autofit simple de columnas).
    """
    df.to_excel(writer, sheet_name=sheet_name, index=index)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Formato numérico
    num_format = workbook.add_format({"num_format": float_format})

    # Aplicar formato de número a todas las columnas numéricas
    for idx, col in enumerate(df.columns, start=1):  # +1 por la columna de índice de Excel
        if pd.api.types.is_numeric_dtype(df[col]):
            worksheet.set_column(idx, idx, 12, num_format)
        else:
            worksheet.set_column(idx, idx, 18)  # ancho por defecto texto

    # Encabezados en negrita
    header_format = workbook.add_format({"bold": True})
    worksheet.set_row(0, None, header_format)


def add_outlet_sales_chart(
    writer: pd.ExcelWriter,
    outlet_kpis: pd.DataFrame,
    sheet_name: str = "Outlet_KPIs",
    chart_sheet_name: str = "Charts",
) -> None:
    """
    Crea un gráfico simple de barras de ventas por OutletID
    y lo inserta en una hoja 'Charts'.
    """
    workbook = writer.book

    # Asegurar que exista la hoja de KPIs de outlet
    if sheet_name not in writer.sheets:
        outlet_kpis.to_excel(writer, sheet_name=sheet_name, index=False)

    # Obtener worksheet de KPIs
    kpi_ws = writer.sheets[sheet_name]

    # Crear hoja de charts si no existe
    if chart_sheet_name in writer.sheets:
        chart_ws = writer.sheets[chart_sheet_name]
    else:
        chart_ws = workbook.add_worksheet(chart_sheet_name)
        writer.sheets[chart_sheet_name] = chart_ws

    # Crear gráfico de columnas
    chart = workbook.add_chart({"type": "column"})

    # Asumimos que OutletID está en la columna A (col 0) y total_sales en la B (col 1)
    max_row = len(outlet_kpis)

    chart.add_series({
        "name":       "Total Sales by Outlet",
        "categories": [sheet_name, 1, 0, max_row, 0],  # A2:A{n}
        "values":     [sheet_name, 1, 1, max_row, 1],  # B2:B{n}
    })

    chart.set_title({"name": "Total Sales by Outlet"})
    chart.set_x_axis({"name": "OutletID"})
    chart.set_y_axis({"name": "Total Sales"})

    # Insertar gráfico en charts sheet
    chart_ws.insert_chart("B2", chart)


def create_excel_report(
    df_enriched: pd.DataFrame,
    kpi_tables: Dict[str, pd.DataFrame],
    output_path: Path | None = None,
    add_chart: bool = True,
) -> Path:
    """
    Crea el archivo Excel con múltiples hojas de reportes.

    Parameters
    ----------
    df_enriched : DataFrame
        Datos a nivel fila, ya limpios y enriquecidos.
    kpi_tables : dict
        Diccionario con tablas de KPIs, por ejemplo:
        {
            "global_kpis": df,
            "outlet_kpis": df,
            "product_type_kpis": df,
            ...
        }
    output_path : Path, opcional
        Ruta completa del archivo de salida. Si es None, se genera
        automáticamente con build_report_filepath().
    add_chart : bool
        Si True, agrega un gráfico simple de ventas por Outlet.

    Returns
    -------
    Path
        Ruta del archivo Excel generado.
    """
    if output_path is None:
        output_path = build_report_filepath()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Crear ExcelWriter con engine xlsxwriter
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        # Hoja principal con datos enriquecidos
        write_df_with_format(writer, df_enriched, sheet_name="Data", index=False)

        # Hojas de KPIs
        for name, table in kpi_tables.items():
            # Normalizar nombre de hoja (máx 31 caracteres en Excel)
            sheet_name = name[:31]
            write_df_with_format(writer, table, sheet_name=sheet_name, index=False)

        # Agregar gráfico si tenemos outlet_kpis
        if add_chart and "outlet_kpis" in kpi_tables:
            add_outlet_sales_chart(
                writer,
                kpi_tables["outlet_kpis"],
                sheet_name="outlet_kpis"[:31],
                chart_sheet_name="Charts",
            )

        # writer.close() implícito por el context manager

    return output_path


def export_csv_summaries(
    kpi_tables: Dict[str, pd.DataFrame],
    folder: Path = Path("reports/csv"),
) -> None:
    """
    Exporta cada tabla de KPIs como CSV separado (opcional).
    """
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    for name, table in kpi_tables.items():
        filename = folder / f"{name}.csv"
        table.to_csv(filename, index=False)