import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "money_exchange.db"

DEFAULT_CURRENCIES = [
    ("USD", "US Dollar", "United States", "$", 1.0),
    ("EUR", "Euro", "European Union", "€", 1.10),
    ("GBP", "British Pound", "United Kingdom", "£", 1.25),
    ("JPY", "Japanese Yen", "Japan", "¥", 0.0070),
    ("CNY", "Chinese Yuan", "China", "¥", 0.14),
]


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def setup_database(conn: sqlite3.Connection):
    sql = [
        """
        CREATE TABLE IF NOT EXISTS Customer(
            c_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone_number TEXT,
            address TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Currency(
            cur_code TEXT PRIMARY KEY,
            cur_name TEXT NOT NULL,
            country TEXT,
            symbol TEXT,
            rate_to_usd REAL NOT NULL,
            last_updated TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Account(
            a_id INTEGER PRIMARY KEY AUTOINCREMENT,
            c_id INTEGER NOT NULL,
            cur_code TEXT NOT NULL,
            account_type TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0,
            FOREIGN KEY(c_id) REFERENCES Customer(c_id),
            FOREIGN KEY(cur_code) REFERENCES Currency(cur_code)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Transactions(
            t_id INTEGER PRIMARY KEY AUTOINCREMENT,
            a_id INTEGER NOT NULL,
            trans_type TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            trans_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(a_id) REFERENCES Account(a_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Exchanges(
            e_id INTEGER PRIMARY KEY AUTOINCREMENT,
            t_id INTEGER NOT NULL,
            a_id INTEGER NOT NULL,
            currency_from TEXT NOT NULL,
            currency_to TEXT NOT NULL,
            amount_from REAL NOT NULL,
            amount_to REAL NOT NULL,
            rate REAL NOT NULL,
            exchange_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            FOREIGN KEY(t_id) REFERENCES Transactions(t_id),
            FOREIGN KEY(a_id) REFERENCES Account(a_id),
            FOREIGN KEY(currency_from) REFERENCES Currency(cur_code),
            FOREIGN KEY(currency_to) REFERENCES Currency(cur_code)
        )
        """,
    ]
    for statement in sql:
        conn.execute(statement)
    conn.commit()


def seed_sample_data(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Customer")
    has_customer = cur.fetchone()[0] > 0
    cur.execute("SELECT COUNT(*) FROM Currency")
    has_currency = cur.fetchone()[0] > 0

    if not has_currency:
        now = datetime.utcnow().isoformat()
        conn.executemany(
            "INSERT INTO Currency(cur_code, cur_name, country, symbol, rate_to_usd, last_updated) VALUES (?, ?, ?, ?, ?, ?)",
            [(code, name, country, symbol, rate, now) for code, name, country, symbol, rate in DEFAULT_CURRENCIES],
        )

    if not has_customer:
        conn.execute(
            "INSERT INTO Customer(first_name, last_name, email, phone_number, address) VALUES (?, ?, ?, ?, ?)",
            ("Alice", "Li", "alice.li@example.com", "+86 138 0013 8000", "Beijing, China"),
        )
        conn.commit()

    cur.execute("SELECT c_id FROM Customer LIMIT 1")
    row = cur.fetchone()
    if row:
        customer_id = row[0]
        cur.execute("SELECT COUNT(*) FROM Account WHERE c_id = ?", (customer_id,))
        if cur.fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO Account(c_id, cur_code, account_type, balance) VALUES (?, ?, ?, ?)",
                [
                    (customer_id, "USD", "checking", 1200.0),
                    (customer_id, "EUR", "savings", 650.0),
                ],
            )
    conn.commit()


def list_customers(conn: sqlite3.Connection):
    rows = conn.execute("SELECT c_id, first_name, last_name, email FROM Customer ORDER BY c_id").fetchall()
    if not rows:
        print("No customers found.")
        return
    print("Customers:")
    for c_id, first_name, last_name, email in rows:
        print(f"  {c_id}: {first_name} {last_name} <{email}>")


def list_accounts(conn: sqlite3.Connection, customer_id: int | None = None):
    query = "SELECT a.a_id, a.c_id, c.first_name, c.last_name, a.cur_code, a.account_type, a.balance FROM Account a JOIN Customer c ON a.c_id=c.c_id"
    params = ()
    if customer_id is not None:
        query += " WHERE a.c_id = ?"
        params = (customer_id,)
    query += " ORDER BY a.a_id"
    rows = conn.execute(query, params).fetchall()
    if not rows:
        print("No accounts found.")
        return
    print("Accounts:")
    for a_id, c_id, first_name, last_name, code, account_type, balance in rows:
        owner = f"{first_name} {last_name}"
        print(f"  {a_id}: {owner} ({code}) {account_type} balance={balance:.2f}")


def list_currencies(conn: sqlite3.Connection):
    rows = conn.execute("SELECT cur_code, cur_name, country, symbol, rate_to_usd FROM Currency ORDER BY cur_code").fetchall()
    print("Supported currencies:")
    for code, name, country, symbol, rate_to_usd in rows:
        print(f"  {code}: {name} ({country}) {symbol} | 1 {code} = {rate_to_usd:.4f} USD")


def choose_customer(conn: sqlite3.Connection) -> int | None:
    customers = conn.execute("SELECT c_id, first_name, last_name FROM Customer ORDER BY c_id").fetchall()
    if not customers:
        print("No customers available.")
        return None
    print("Available customers:")
    for c_id, first_name, last_name in customers:
        print(f"  {c_id}: {first_name} {last_name}")
    while True:
        selected = input("Enter customer ID: ").strip()
        if selected.isdigit():
            return int(selected)
        print("Invalid input. Please enter a numeric customer ID.")


def choose_currency(conn: sqlite3.Connection, prompt: str) -> str | None:
    codes = [row[0] for row in conn.execute("SELECT cur_code FROM Currency ORDER BY cur_code").fetchall()]
    if not codes:
        print("No currency definitions available.")
        return None
    print(prompt)
    print("Supported codes:", ", ".join(codes))
    while True:
        code = input("Currency code: ").strip().upper()
        if code in codes:
            return code
        print("Unsupported currency, please use one of:", ", ".join(codes))


def get_rate(conn: sqlite3.Connection, code: str) -> float:
    row = conn.execute("SELECT rate_to_usd FROM Currency WHERE cur_code = ?", (code,)).fetchone()
    return float(row[0]) if row else 0.0


def find_account(conn: sqlite3.Connection, customer_id: int, cur_code: str):
    return conn.execute(
        "SELECT a_id, balance FROM Account WHERE c_id = ? AND cur_code = ?",
        (customer_id, cur_code),
    ).fetchone()


def create_account(conn: sqlite3.Connection, customer_id: int, cur_code: str, balance: float = 0.0):
    conn.execute(
        "INSERT INTO Account(c_id, cur_code, account_type, balance) VALUES (?, ?, ?, ?)",
        (customer_id, cur_code, "exchange", balance),
    )
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def perform_conversion(conn: sqlite3.Connection):
    customer_id = choose_customer(conn)
    if customer_id is None:
        return
    list_accounts(conn, customer_id)
    currency_from = choose_currency(conn, "Select source currency:")
    if currency_from is None:
        return
    currency_to = choose_currency(conn, "Select destination currency:")
    if currency_to is None:
        return
    if currency_from == currency_to:
        print("Source and destination currency are the same. No conversion needed.")
        return
    amount_str = input(f"Amount to convert from {currency_from}: ").strip()
    try:
        amount_from = float(amount_str)
        if amount_from <= 0:
            raise ValueError
    except ValueError:
        print("Enter a valid positive amount.")
        return

    source_account = find_account(conn, customer_id, currency_from)
    if not source_account:
        print(f"No account found for customer {customer_id} in {currency_from}.")
        return
    source_aid, source_balance = source_account
    if amount_from > source_balance:
        print(f"Insufficient funds: account balance is {source_balance:.2f} {currency_from}.")
        return

    rate_from = get_rate(conn, currency_from)
    rate_to = get_rate(conn, currency_to)
    if rate_from <= 0 or rate_to <= 0:
        print("Unable to determine exchange rates for selected currencies.")
        return

    rate = rate_from / rate_to
    amount_to = round(amount_from * rate, 2)
    if amount_to <= 0:
        print("Converted amount is zero or invalid.")
        return

    target_account = find_account(conn, customer_id, currency_to)
    if target_account is None:
        print(f"No target account in {currency_to} found. A new account will be created.")
        target_aid = create_account(conn, customer_id, currency_to, 0.0)
    else:
        target_aid = target_account[0]

    new_source_balance = source_balance - amount_from
    conn.execute("UPDATE Account SET balance = ? WHERE a_id = ?", (new_source_balance, source_aid))

    target_balance = 0.0
    if target_account is not None:
        target_balance = target_account[1]
    new_target_balance = target_balance + amount_to
    conn.execute("UPDATE Account SET balance = ? WHERE a_id = ?", (new_target_balance, target_aid))

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Transactions(a_id, trans_type, amount, status) VALUES (?, ?, ?, ?)",
        (source_aid, "exchange", amount_from, "completed"),
    )
    transaction_id = cur.lastrowid
    cur.execute(
        "INSERT INTO Exchanges(t_id, a_id, currency_from, currency_to, amount_from, amount_to, rate, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (transaction_id, source_aid, currency_from, currency_to, amount_from, amount_to, rate, "completed"),
    )
    conn.commit()

    print("Conversion complete:")
    print(f"  {amount_from:.2f} {currency_from} -> {amount_to:.2f} {currency_to}")
    print(f"  Exchange rate: 1 {currency_from} = {rate:.6f} {currency_to}")
    print(f"  New source balance: {new_source_balance:.2f} {currency_from}")
    print(f"  New target balance: {new_target_balance:.2f} {currency_to}")


def show_history(conn: sqlite3.Connection):
    rows = conn.execute(
        "SELECT e.e_id, e.exchange_date, e.currency_from, e.currency_to, e.amount_from, e.amount_to, e.rate, e.status, c.first_name, c.last_name "
        "FROM Exchanges e "
        "JOIN Transactions t ON e.t_id = t.t_id "
        "JOIN Account a ON e.a_id = a.a_id "
        "JOIN Customer c ON a.c_id = c.c_id "
        "ORDER BY e.exchange_date DESC"
    ).fetchall()
    if not rows:
        print("No exchange history found.")
        return
    print("Exchange history:")
    for e_id, exchange_date, cur_from, cur_to, amt_from, amt_to, rate, status, first_name, last_name in rows:
        print(f"  {e_id}: {exchange_date} | {first_name} {last_name} | {amt_from:.2f} {cur_from} -> {amt_to:.2f} {cur_to} | rate={rate:.6f} | {status}")


def main_menu():
    conn = connect_db()
    setup_database(conn)
    seed_sample_data(conn)

    actions = {
        "1": ("List customers", lambda: list_customers(conn)),
        "2": ("List accounts", lambda: list_accounts(conn)),
        "3": ("List currencies", lambda: list_currencies(conn)),
        "4": ("Convert currency", lambda: perform_conversion(conn)),
        "5": ("Show exchange history", lambda: show_history(conn)),
        "0": ("Exit", None),
    }

    while True:
        print("\nCurrency Exchange Menu")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        choice = input("Select an option: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            action[1]()
        else:
            print("Invalid selection.")

    conn.close()


if __name__ == "__main__":
    main_menu()
