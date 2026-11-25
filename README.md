# Retail ETL

A beginner-friendly Python project for processing retail CSV files.

## Project folders

- `src/` contains the ETL script.
- `tests/` contains automated tests.
- `data/raw/` is where you put source CSV files.
- `data/processed/` is where processed CSV files are written.
- `db/` is reserved for local database files.
- `docs/` is reserved for project documentation.

## Run the project

Run these commands from the project root in PowerShell:

1. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

2. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Put one or more `.csv` files in `data/raw/`, then run the ETL script:

   ```powershell
   python -m src.etl
   ```

   The script trims whitespace from CSV column names and writes the result to
   `data/processed/`. If `data/raw/` has no CSV files, it prints a message and
   exits without an error.

5. Run the tests:

   ```powershell
   python -m pytest
   ```