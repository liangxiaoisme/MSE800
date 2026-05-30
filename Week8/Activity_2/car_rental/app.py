import sqlite3
import sys

DB_NAME = "cars.db"

MENU = """
=== Car Rental System ===
1. Add Car
2. List Cars
3. Remove Car
4. Exit
=======================
Choose an option: """


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            plate TEXT PRIMARY KEY,
            car_type TEXT NOT NULL,
            year INTEGER NOT NULL CHECK(year >= 1886)
        )
    """)
    conn.commit()
    conn.close()


def add_car(plate, car_type, year):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO cars (plate, car_type, year) VALUES (?, ?, ?)",
            (plate.strip().upper(), car_type.strip(), int(year)),
        )
        conn.commit()
        print(f"✅ Car {plate.strip().upper()} added successfully!")
    except sqlite3.IntegrityError:
        print("❌ Car with this plate already exists!")
    finally:
        conn.close()


def list_cars():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT plate, car_type, year FROM cars ORDER BY plate")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("(no cars found)")
        return

    print(f"{'Plate':<12} {'Type':<12} {'Year':<6}")
    print("-" * 30)
    for plate, car_type, year in rows:
        print(f"{plate:<12} {car_type:<12} {year:<6}")


def remove_car(plate):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM cars WHERE plate = ?", (plate.strip().upper(),))
    conn.commit()
    if cur.rowcount:
        print(f"✅ Car {plate.strip().upper()} removed successfully!")
    else:
        print("❌ Car not found!")
    conn.close()


def main():
    create_table()
    while True:
        try:
            choice = input(MENU).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if choice == "1":
            plate = input("Plate: ").strip()
            car_type = input("Type: ").strip()
            try:
                year = int(input("Year: ").strip())
            except ValueError:
                print("❌ Invalid year! Must be a number.")
                continue
            add_car(plate, car_type, year)
        elif choice == "2":
            list_cars()
        elif choice == "3":
            plate = input("Plate to remove: ").strip()
            remove_car(plate)
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
