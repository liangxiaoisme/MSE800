from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "W4Act1.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    user_fullname TEXT,
    user_phone INTEGER,
    user_registration_date TEXT,
    user_email TEXT UNIQUE
);
                     
CREATE TABLE IF NOT EXISTS currency (
    currency_id INTEGER PRIMARY KEY,
    currency_name TEXT,
    currency_code TEXT UNIQUE,
    currency_symbol TEXT,
    currency_country TEXT
);
                     
CREATE TABLE IF NOT EXISTS exchangeRate (
    exchange_id INTEGER PRIMARY KEY,
    from_currency_id INTEGER,
    to_currency_id INTEGER,
    exchange_rate REAL,
    exchange_date TEXT
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    exchange_id INTEGER,
    transaction_fee REAL,
    transaction_amount_from REAL,
    transaction_amount_to REAL,
    transaction_date TEXT,
    transaction_status TEXT
);
                     
CREATE TABLE IF NOT EXISTS log (
    log_id INTEGER PRIMARY KEY,
    transaction_id INTEGER,
    timestamp TEXT,
    transaction_status TEXT,
    status_message TEXT
);
''')

conn.commit()


cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Database path:", DB_PATH)
print("\nTables and columns:")

for table in tables:
    table_name = table[0]
    print(f"\nTable: {table_name}")

    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    for column in columns:
        column_id = column[0]
        column_name = column[1]
        column_type = column[2]
        not_null = column[3]
        default_value = column[4]
        primary_key = column[5]

        print(f"  - {column_name} ({column_type})")

conn.close()
