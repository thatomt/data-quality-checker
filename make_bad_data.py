import sqlite3
import pandas as pd

# Read the good data
conn = sqlite3.connect("weather.db")
table = pd.read_sql("SELECT * FROM weather", conn)
conn.close()

# Break it on purpose:
# Duplicate the first row (fake duplicate date)
table = pd.concat([table, table.iloc[[0]]], ignore_index=True)

# 2. Make row 2's max_temp lower than its min_temp (impossible)
table.loc[2, "max_temp_c"] = 5.0
table.loc[2, "min_temp_c"] = 20.0

# Add a wild outlier temperature
table.loc[3, "max_temp_c"] = 80.0

# Blank out a rain value (missing data)
table.loc[4, "rain_mm"] = None

# Save this broken version as a separate database file
conn = sqlite3.connect("weather_bad.db")
table.to_sql("weather", conn, if_exists="replace", index=False)
conn.close()

print("Done. Created weather_bad.db with 4 deliberate problems.")