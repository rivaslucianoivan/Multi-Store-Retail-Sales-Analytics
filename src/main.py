from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from load_data import load_all_stores
from cleaning import clean_sales_data, build_data_quality_report
from transformations import (
    enrich_sales_data,
    compute_all_kpi_tables,
)
from reporting import create_excel_report, export_csv_summaries


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the reporting pipeline.
    """
    parser = argparse.ArgumentParser(
        description="Multi-Store Retail Sales Analytics - Reporting Pipeline"
    )

    parser.add_argument(
        "--input-dir",
        type=str,
        default="data/raw/stores",
        help="Directory with store-level CSV files (default: data/raw/stores)",
    )

    parser.add_argument(
        "--reports-dir",
        type=str,
        default="reports/final",
        help="Directory where the Excel report will be saved (default: reports/final)",
    )

    parser.add_argument(
        "--reference-year",
        type=int,
        default=2026,
        help="Reference year to compute OutletAge (default: 2026)",
    )

    parser.add_argument(
        "--no-charts",
        action="store_true",
        help="Disable chart generation inside the Excel report",
    )

    parser.add_argument(
        "--export-csv",
        action="store_true",
        help="Also export KPI tables as separate CSV files (reports/csv)",
    )

    return parser.parse_args()


def run_pipeline(
    input_dir: Path,
    reports_dir: Path,
    reference_year: int = 2026,
    add_charts: bool = True,
    export_csv: bool = False,
) -> Dict[str, Any]:
    """
    Run the full data pipeline: load -> clean -> enrich -> KPIs -> reports.

    Parameters
    ----------
    input_dir : Path
        Folder containing store-level CSV files.
    reports_dir : Path
        Folder where the Excel report will be saved.
    reference_year : int
        Year used to compute OutletAge.
    add_charts : bool
        Whether to add charts to the Excel report.
    export_csv : bool
        Whether to export KPI tables as individual CSV files.

    Returns
    -------
    dict
        Dictionary with key pipeline objects and paths.
    """
    input_dir = Path(input_dir)
    reports_dir = Path(reports_dir)

    print("=== Multi-Store Retail Sales Analytics ===")
    print(f"Input directory  : {input_dir.resolve()}")
    print(f"Reports directory: {reports_dir.resolve()}")
    print(f"Reference year   : {reference_year}")
    print("-------------------------------------------")

    # 1) Load data
    print("Step 1/5 - Loading store data...")
    df_raw: pd.DataFrame = load_all_stores(raw_dir=input_dir)
    print(f"  Raw data shape: {df_raw.shape}")

    # 2) Clean data
    print("Step 2/5 - Cleaning data...")
    df_clean: pd.DataFrame = clean_sales_data(df_raw)
    dq_report: pd.DataFrame = build_data_quality_report(df_raw, df_clean)
    print("  Data quality report:")
    print(dq_report.to_string(index=False))

    # 3) Enrich data (feature engineering)
    print("Step 3/5 - Enriching data (OutletAge, PriceSegment, SalesShare)...")
    df_enriched: pd.DataFrame = enrich_sales_data(df_clean, reference_year=reference_year)
    print(f"  Enriched data shape: {df_enriched.shape}")

    # 4) Compute KPI tables
    print("Step 4/5 - Computing KPI tables...")
    kpi_tables: Dict[str, pd.DataFrame] = compute_all_kpi_tables(df_enriched)
    for name, table in kpi_tables.items():
        print(f"  {name}: {table.shape[0]} rows, {table.shape[1]} columns")

    # 5) Generate reports
    print("Step 5/5 - Generating reports...")
    report_path = create_excel_report(
        df_enriched=df_enriched,
        kpi_tables=kpi_tables,
        output_path=reports_dir / "retail_sales_report.xlsx",
        add_chart=add_charts,
    )
    print(f"  Excel report saved to: {report_path}")

    if export_csv:
        print("  Exporting KPI tables as CSV...")
        export_csv_summaries(kpi_tables)

    print("Pipeline completed successfully.")

    return {
        "df_raw": df_raw,
        "df_clean": df_clean,
        "df_enriched": df_enriched,
        "dq_report": dq_report,
        "kpi_tables": kpi_tables,
        "report_path": report_path,
    }


def main() -> None:
    """
    CLI entry point.
    """
    args = parse_args()

    run_pipeline(
        input_dir=Path(args.input_dir),
        reports_dir=Path(args.reports_dir),
        reference_year=args.reference_year,
        add_charts=not args.no_charts,
        export_csv=args.export_csv,
    )


if __name__ == "__main__":
    main()