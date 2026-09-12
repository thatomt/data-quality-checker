import sqlite3
import sys
import pandas as pd


db_file = sys.argv[1] if len(sys.argv) > 1 else "weather.db"
print(f"Checking file: {db_file}\n")

# Read the weather table from the database
conn = sqlite3.connect(db_file)
table = pd.read_sql("SELECT * FROM weather", conn)
conn.close()

print(f"Loaded {len(table)} rows.\n")

problems_found = 0

# Check 1: missing values
missing = table.isnull().sum()
missing = missing[missing > 0]
if len(missing) > 0:
    print("MISSING VALUES:")
    print(missing)
    problems_found += 1
else:
    print("No missing values found.")

# Check 2: duplicate rows (same date appearing twice)
duplicates = table[table.duplicated(subset=["date"], keep=False)]
if len(duplicates) > 0:
    print("\nDUPLICATE DATES:")
    print(duplicates)
    problems_found += 1
else:
    print("No duplicate dates found.")

# Check 3: max temp lower than min temp (physically impossible)
bad_temps = table[table["max_temp_c"] < table["min_temp_c"]]
if len(bad_temps) > 0:
    print("\nROWS WHERE MAX TEMP IS LOWER THAN MIN TEMP (impossible):")
    print(bad_temps)
    problems_found += 1
else:
    print("No rows with max temp lower than min temp.")

# Check 4: outlier temperatures (way outside a realistic range)
outliers = table[(table["max_temp_c"] > 50) | (table["min_temp_c"] < -20)]
if len(outliers) > 0:
    print("\nOUTLIER TEMPERATURES (outside -20C to 50C):")
    print(outliers)
    problems_found += 1
else:
    print("No outlier temperatures found.")


print("\n--- SUMMARY ---")
if problems_found == 0:
    print("All checks passed. Data looks clean.")
else:
    print(f"{problems_found} type(s) of problem found. See details above.")