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

# Check for any missing values
missing = table.isnull().sum()
missing = missing[missing > 0]
if len(missing) > 0:
    print("MISSING VALUES:")
    print(missing)
    problems_found += 1
else:
    print("No missing values found.")