# data-quality-checker

A script that checks a weather database for common data quality problems:
missing values, duplicate rows, and physically impossible or outlier values.

Built as a follow-on to [weather-data-pipeline](https://github.com/thatomt/Weather-data-pipeline), this
project takes the data produced by that pipeline and validates it before it
would be trusted for reporting or analysis.

## How it works

`check_quality.py` reads a SQLite database table and runs four checks:

1. **Missing values** — are any cells empty?
2. **Duplicate dates** — does the same date appear more than once?
3. **Impossible values** — is the max temperature lower than the min
   temperature for the same day?
4. **Outliers** — are any temperatures outside a realistic range
   (-20C to 50C)?

It prints a report showing exactly what was found, and a one-line summary
at the end.

## Proving it actually works

`make_bad_data.py` takes the real weather data and deliberately breaks it —
adding a duplicate row, an impossible temperature pair, an outlier, and a
missing value — then saves it as a separate file (`weather_bad.db`) so the
original data is never touched.

Running the checker against this file confirms all four planted problems
are correctly caught.

## How to run it

```bash
pip install pandas

# Check real data (should come back clean)
python check_quality.py weather.db

# Create deliberately broken data
python make_bad_data.py

# Check the broken data (should catch all 4 planted problems)
python check_quality.py weather_bad.db
```

## Tech used

- Python
- `pandas` — data checks and manipulation
- `sqlite3` — reading the database

## Possible next steps

- Add more checks (e.g. date gaps, unrealistic rainfall values)
- Turn the report into a saved file (e.g. CSV or HTML) instead of just
  printing to the terminal
- Run automatically every time new data lands, as part of a pipeline