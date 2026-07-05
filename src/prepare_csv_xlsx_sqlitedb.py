import os
import pandas as pd
import sqlite3

folder_path = "data/csv_xlsx"
db_path = "data/csv_xlsx_sqldb.db"

conn = sqlite3.connect(db_path)

for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)

    if file.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    else:
        continue

    table_name = os.path.splitext(file)[0]
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"{table_name} loaded successfully")

conn.close()
print("Database created successfully!")