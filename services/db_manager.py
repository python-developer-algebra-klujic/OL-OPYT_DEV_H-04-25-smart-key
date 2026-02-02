import sqlite3

from constants.ui_constants import DATABASE_PATH



def db_init():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                   (
                        id INTEGER PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        pin TEXT CHECK(length(pin) <= 4),
                        is_active INTEGER DEFAULT 0 CHECK(is_active IN (0, 1))
                    )''')

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if len(users) <= 0:
        cursor.execute('''INSERT INTO users (first_name, last_name, pin, is_active)
                       VALUES (?, ?, ?, ?)''',
                       ('Administrator', 'Admin', '1234', 1))

    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Query the database to fetch data
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return users


def create_user(first_name: str,
                last_name: str,
                pin: str,
                is_active: bool,
                id: int = 0):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    if id == 0:
        if is_active:
            is_active_val = 1
        else:
            is_active_val = 0
        cursor.execute('''INSERT INTO users (first_name, last_name, pin, is_active)
                       VALUES (?, ?, ?, ?)''',
                       (first_name, last_name, pin, is_active_val))
    else:
        cursor.execute("SELECT * FROM users WHERE id is ?", (id,))
        user = cursor.fetchall()

        # Update user
        if is_active:
            is_active_val = 1
        else:
            is_active_val = 0
        cursor.execute('''UPDATE users
                       SET first_name = ?, last_name = ?, pin = ?, is_active = ?
                       WHERE id = ?''',
                       (first_name, last_name, pin, is_active, id))
    conn.commit()
    conn.close()


def delete_user(id: int):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM users WHERE id = ?''', (id,))

    conn.commit()
    conn.close()