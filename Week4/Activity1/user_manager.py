from database import create_connection


def add_user(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    print(f"User '{name}' added.")


def view_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_user(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users WHERE name LIKE ?", ('%' + name + '%',))
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    print(f"User ID {user_id} deleted.")
