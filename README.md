# Multi-Store Retail Sales Analytics

Python project for consolidating multi-store retail sales files, cleaning inconsistencies, engineering features, calculating KPIs, and generating business-ready Excel reports.

## Project Overview

Retail companies often receive sales data from multiple stores in separate CSV files.  
Before analysis, these files need to be standardized, cleaned, merged, enriched with new features, and transformed into clear KPI reports.

This project simulates that real-world workflow using Python and pandas.  
The goal is to build an automated analytics and reporting pipeline that:

- Loads sales files from multiple stores.
- Cleans and standardizes the data.
- Enriches the dataset with additional features for analysis.
- Calculates KPIs and summary tables.
- Exports a multi-sheet Excel report ready for business stakeholders.

## Business Problem

A retail chain receives sales data from several stores, each one exporting its own file.  
The company needs a repeatable process to consolidate all files into a single clean dataset and generate reports such as:

- Total sales by store.
- Average sales per record.
- Sales by product type and fat content.
- Top-selling products across the chain.
- Performance by outlet type and price segment.
- Data quality checks (rows removed, nulls, duplicates).

Without automation, this process is manual, slow, and error‑prone.

## Dataset

The project uses the **Big Mart Sales** dataset (train file), which contains multiple outlets identified by `OutletID`.  
The original file is split into store-level CSV files (one per outlet) that simulate the real situation where each store sends its own export.

Main columns used in the pipeline:

- `ProductID`
- `Weight`
- `FatContent`
- `ProductVisibility`
- `ProductType`
- `MRP`
- `OutletID`
- `EstablishmentYear`
- `OutletSize`
- `LocationType`
- `OutletType`
- `OutletSales`

## Project Goals

- Build a clean, modular Python project.
- Practice data cleaning, feature engineering, and aggregation with pandas.
- Simulate a real reporting task for a multi-store retail business.
- Produce portfolio-ready outputs for Data Analyst / Data Science roles.

## Tech Stack

- Python
- pandas
- NumPy
- matplotlib / seaborn (optional for extra visuals)
- XlsxWriter (Excel reporting engine)[^xlsxwriter]
- openpyxl
- Jupyter Notebook (exploration)
- pytest (basic tests)

[^xlsxwriter]: The project uses `pandas.ExcelWriter` with the `xlsxwriter` engine to generate multi-sheet Excel files and apply simple formatting.[web:107][web:119]

## Project Structure

```bash
Multi-Store-Retail-Sales-Analytics/
│
├── data/
│   ├── raw/
│   │   └── stores/          # One CSV per store (OutletID)
│   └── processed/           # (optional) intermediate files
│
├── notebooks/               # EDA and experimentation
│
├── reports/
│   ├── figures/             # (optional) PNG charts
│   ├── final/               # Final Excel reports
│   └── csv/                 # Exported KPI tables as CSV
│
├── src/
│   ├── load_data.py         # Data loading and consolidation
│   ├── cleaning.py          # Data cleaning and standardization
│   ├── transformations.py   # Feature engineering + KPI tables
│   ├── reporting.py         # Excel report and CSV export
│   └── main.py              # Orchestration / CLI entry point
│
├── tests/                   # pytest unit tests (optional but recommended)
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Data Pipeline

The end-to-end pipeline is orchestrated by `src/main.py`:

1. **Load**  
   - Combines all store-level CSV files from `data/raw/stores/` into a single DataFrame.  
   - Adds metadata such as `source_file` if needed.

2. **Clean**  
   - Standardizes column names to the canonical schema (e.g., `item_mrp` → `MRP`).  
   - Normalizes text fields (e.g., `FatContent`: `LF`, `low fat` → `Low Fat`).  
   - Converts numeric columns (`Weight`, `ProductVisibility`, `MRP`, `OutletSales`) to proper types.  
   - Handles missing values (e.g., impute `Weight` by product median, fill `OutletSize` with mode).  
   - Removes duplicates and filters out invalid records (negative or zero values where they make no sense).

3. **Enrich (Feature Engineering)**  
   - Adds `OutletAge` from `EstablishmentYear` and a reference year.  
   - Creates `PriceSegment` (Low / Medium / High / Premium) from `MRP`.  
   - Computes `SalesShare` (row-level contribution to total sales).

4. **KPIs & Aggregations**  
   - Global KPIs (total sales, total outlets, total products, average MRP, etc.).  
   - KPIs by `OutletID` (sales, average sales, unique products, average MRP, visibility, age).  
   - KPIs by `ProductType`, `FatContent`, `OutletType`, and `PriceSegment`.  
   - Top N products by total sales across all outlets.

5. **Reporting**  
   - Generates a multi-sheet Excel report using `pandas.ExcelWriter` with the `xlsxwriter` engine.[web:107][web:119]  
   - Exports each KPI table to its own sheet and includes the enriched data in a `Data` sheet.  
   - Optionally adds a simple chart (e.g., total sales by outlet) in a `Charts` sheet.  
   - Optionally exports all KPI tables as separate CSV files in `reports/csv/`.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Multi-Store-Retail-Sales-Analytics.git
cd Multi-Store-Retail-Sales-Analytics
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Make sure `XlsxWriter` is installed, as it is required by the Excel reporting module.[web:119]

### 4. Prepare the data

Place the store-level CSV files in:

```bash
data/raw/stores/
```

Each file should correspond to a single outlet (`OutletID`), for example:

- `outlet_OUT049.csv`
- `outlet_OUT018.csv`
- `outlet_OUT027.csv`
- ...

### 5. Run the full pipeline

From the **project root**:

```bash
python src/main.py
```

This will:

- Load all CSVs from `data/raw/stores/`.  
- Clean and enrich the data.  
- Compute KPI tables.  
- Generate an Excel report in `reports/final/retail_sales_report.xlsx`.

### 6. Command-line options

`main.py` includes a small CLI:

```bash
python src/main.py --help
```

Parámetros soportados:

- `--input-dir`: directory with store CSVs (default: `data/raw/stores`).  
- `--reports-dir`: directory where the Excel report is saved (default: `reports/final`).  
- `--reference-year`: year used to compute `OutletAge` (default: 2026).  
- `--no-charts`: disable chart creation inside the Excel file.  
- `--export-csv`: also export KPI tables to `reports/csv/` as separate CSV files.

Ejemplos:

```bash
# Run with defaults
python src/main.py

# Run without charts and export individual CSVs
python src/main.py --no-charts --export-csv

# Custom input and reports directories
python src/main.py --input-dir data/raw/stores --reports-dir output/reports
```

## Outputs

Main outputs:

- **Excel report**  
  - Location: `reports/final/retail_sales_report.xlsx`  
  - Sheets:
    - `Data` – enriched row-level dataset.  
    - `global_kpis` – one-row table with overall metrics.  
    - `outlet_kpis` – metrics by `OutletID`.  
    - `product_type_kpis` – metrics by `ProductType`.  
    - `fat_content_kpis` – metrics by `FatContent`.  
    - `outlet_type_kpis` – metrics by `OutletType`.  
    - `price_segment_kpis` – metrics by `PriceSegment`.  
    - `top_products` – top N products by total sales.  
    - `Charts` – simple Excel chart (e.g., total sales by outlet), if chart generation is enabled.

- **Optional CSVs**  
  - Location: `reports/csv/`  
  - One `.csv` file per KPI table when `--export-csv` is used.

## Testing

Basic tests are set up using **pytest**.[web:123][web:122]

### Run tests

From the project root:

```bash
pytest
```

Example tests include:

- `test_load_data.py` – checks that store files are loaded and combined correctly.  
- `test_cleaning.py` – verifies that the cleaning pipeline removes invalid values and keeps expected columns.  
- `test_transformations.py` – ensures that enrichment adds `OutletAge`, `PriceSegment`, `SalesShare` and that KPI tables are generated.  
- `test_reporting.py` – verifies that the Excel report is created successfully.

## Possible Extensions

Ideas for future improvements:

- Add visualizations (matplotlib/seaborn) and export them as PNGs into `reports/figures/`.  
- Build a simple Streamlit or Dash app to explore the KPIs interactively.  
- Add more advanced data quality checks (outlier detection, distribution analysis).  
- Extend the project to handle daily transactional data with a real `Date` column and time-series trends.  
- Add more comprehensive unit tests and CI configuration (e.g., GitHub Actions).

## Author

**Luciano Rivas**  
Aspiring Data Analyst / Data Scientist focused on Python, pandas, automation, and business reporting projects.
