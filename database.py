import sqlite3

def create_connection():
    return sqlite3.connect("money_exchange.db")

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Currencies (
            currency_id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_code TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            currency_from INTEGER NOT NULL,
            currency_to INTEGER NOT NULL,
            amount_from REAL NOT NULL,
            amount_to REAL NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (currency_from) REFERENCES Currencies(currency_id),
            FOREIGN KEY (currency_to) REFERENCES Currencies(currency_id)
        )
    ''')
    
    conn.commit()
    conn.close()
