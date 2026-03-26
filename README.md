# Multi-Store Retail Sales Analytics

Python project for consolidating multi-store retail sales files, cleaning inconsistencies, removing duplicates, standardizing formats, and generating business-ready KPI reports.

## Project Overview

Retail companies often receive sales files from multiple stores in separate CSV or Excel files.  
Before analysis, these files usually need to be standardized, cleaned, merged, and validated.

This project simulates that real-world workflow using Python and pandas.  
The goal is to build an automated reporting pipeline that:

- Loads sales files from multiple stores.
- Cleans and standardizes the data.
- Removes duplicates and invalid records.
- Creates KPIs and summary tables.
- Exports final reports for business use.

## Business Problem

A retail chain receives sales data from several stores, each one exporting its own file.  
The company needs a repeatable process to consolidate all files into a single clean dataset and generate reports such as:

- Total sales by store.
- Average ticket by store.
- Sales by product category.
- Top-selling products.
- Monthly sales trends.
- Data quality checks.

Without automation, this process is manual, slow, and error-prone.

## Dataset

This project uses the **Big Mart Sales** dataset and works mainly with the training file.  
The dataset includes multiple stores identified by the `Outlet_Identifier` field, which makes it suitable for simulating a multi-store reporting workflow.

## Project Goals

- Build a clean and modular Python project.
- Practice data cleaning and transformation with pandas.
- Simulate a real reporting task for a retail business.
- Create portfolio-ready outputs for Data Analyst / Data Science roles.

## Tech Stack

- Python
- pandas
- NumPy
- matplotlib / seaborn
- openpyxl or xlsxwriter
- Jupyter Notebook
- Git and GitHub

## Planned Workflow

1. Load the original sales dataset.
2. Split the data into separate files by `Outlet_Identifier`.
3. Read all store files from a folder.
4. Standardize column names and data types.
5. Clean missing values and inconsistent records.
6. Remove duplicates.
7. Create derived metrics and business KPIs.
8. Generate summary tables and visual reports.
9. Export final outputs to Excel and/or CSV.

## Project Structure

```bash
Multi-Store-Retail-Sales-Analytics/
│
├── data/
│   ├── raw/
│   │   └── stores/
│   └── processed/
│
├── notebooks/
│
├── reports/
│   ├── figures/
│   └── final/
│
├── src/
│   ├── load_data.py
│   ├── cleaning.py
│   ├── transformations.py
│   ├── reporting.py
│   └── main.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Main Features

- Split a retail dataset into multiple store-level CSV files.
- Combine all store files into one consolidated DataFrame.
- Clean and validate the data automatically.
- Generate store-level and overall KPIs.
- Export reports in a professional format.

## Example KPIs

Some of the metrics planned for this project include:

- Total sales
- Number of transactions
- Average sales per item
- Sales by outlet
- Sales by item type
- Monthly sales performance
- Best-performing outlets
- Duplicate and missing-value checks

## How to Run

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

### 4. Run the project

```bash
python src/main.py
```

## Current Status

This project is currently in development.  
The first stage focuses on preparing the dataset, splitting files by store, and building the data cleaning pipeline.

## Future Improvements

- Add automated Excel report formatting.
- Create visual dashboards.
- Include unit tests for cleaning functions.
- Add logging and error handling.
- Build a Streamlit dashboard for report exploration.

## Author

Luciano Rivas

Aspiring Data Analyst / Data Scientist focused on Python, pandas, automation, and business reporting projects.
