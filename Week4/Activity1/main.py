import sqlite3
from database import create_table, create_connection

def menu():
    print("\n==== Money Exchange ====")
    print("1. Add User")
    print("2. Add Currency")
    print("3. Exchange Currency")
    print("4. Exit")

def add_user():
    name = input("User name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (user_name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    print("User added.")

def add_currency():
    code = input("Currency code (e.g. USD): ").strip().upper()
    if not code:
        print("Code cannot be empty.")
        return
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Currencies (currency_code) VALUES (?)", (code,))
        conn.commit()
        print("Currency added.")
    except sqlite3.IntegrityError:
        print("Currency already exists.")
    finally:
        conn.close()

def exchange_currency():
    user_id = input("User ID: ").strip()
    from_code = input("From currency: ").strip().upper()
    to_code = input("To currency: ").strip().upper()
    amount = input("Amount: ").strip()

    if not user_id.isdigit():
        print("Invalid user ID.")
        return
    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT currency_id FROM Currencies WHERE currency_code = ?", (from_code,))
    from_id = cursor.fetchone()
    cursor.execute("SELECT currency_id FROM Currencies WHERE currency_code = ?", (to_code,))
    to_id = cursor.fetchone()

    if not from_id or not to_id:
        print("Currency not found.")
        conn.close()
        return

    rate_text = input("Exchange rate: ").strip()
    try:
        rate = float(rate_text)
    except ValueError:
        print("Invalid rate.")
        conn.close()
        return

    amount_to = amount * rate
    cursor.execute(
        "INSERT INTO Transactions (user_id, currency_from, currency_to, amount_from, amount_to) VALUES (?, ?, ?, ?, ?)",
        (int(user_id), from_id[0], to_id[0], amount, amount_to)
    )
    conn.commit()
    conn.close()
    print(f"{amount:.2f} {from_code} = {amount_to:.2f} {to_code}")

def main():
    create_table()
    while True:
        menu()
        choice = input("Option (1-4): ").strip()
        if choice == '1':
            add_user()
        elif choice == '2':
            add_currency()
        elif choice == '3':
            exchange_currency()
        elif choice == '4':
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
