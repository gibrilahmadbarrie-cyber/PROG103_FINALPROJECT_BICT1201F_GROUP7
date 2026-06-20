import sqlite3

DATABASE_NAME = "clinic_records.db"


def connect_db():
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        status TEXT NOT NULL,
        contact TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_record(full_name, gender, status, contact):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO records
    (full_name, gender, status, contact)
    VALUES (?, ?, ?, ?)
    """, (full_name, gender, status, contact))

    conn.commit()
    conn.close()


def get_records():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records")

    records = cursor.fetchall()

    conn.close()

    return records


def delete_record(record_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM records WHERE id=?",
        (record_id,)
    )

    conn.commit()
    conn.close()


def search_records(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM records
    WHERE full_name LIKE ?
    OR status LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    records = cursor.fetchall()

    conn.close()

    return records



def filter_records(gender, status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM records
    WHERE gender LIKE ?
    AND status LIKE ?
    """, (f"%{gender}%", f"%{status}%"))

    records = cursor.fetchall()

    conn.close()

    return records


def insert_sample_records():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM records")

    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()
        return

    sample_data = [

        ("Gibril Ahmad Barrie", "Male", "Active", "076111111"),
        ("Daniel Michael Foffanah", "Male", "Active", "076111111"),
        ("Mariama Sesay", "Female", "Active", "076111112"),
        ("Ibrahim Bah", "Male", "Pending", "076111113"),
        ("Hawa Koroma", "Female", "Inactive", "076111114"),
        ("Alex Jacob", "Male", "Active", "076111115"),
        ("Fatmata Turay", "Female", "Pending", "076111116"),
        ("Mohamed Bangura", "Male", "Active", "076111117"),
        ("Aminata Kanu", "Female", "Active", "076111118"),
        ("Samuel Kargbo", "Male", "Inactive", "076111119"),
        ("Isatu Jalloh", "Female", "Active", "076111120"),
        ("Musa Koroma", "Male", "Pending", "076111121"),
        ("Kadiatu Bah", "Female", "Active", "076111122"),
        ("Sorie Bangura", "Male", "Inactive", "076111123"),
        ("Aisha Turay", "Female", "Active", "076111124"),
        ("Alhaji Kamara", "Male", "Pending", "076111125"),
        ("Mabinty Sesay", "Female", "Active", "076111126"),
        ("Joseph Fofanah", "Male", "Inactive", "076111127"),
        ("Adama Kamara", "Female", "Pending", "076111128"),
        ("Mohamed Kallon", "Male", "Active", "076111129"),
        ("Haja Conteh", "Female", "Active", "076111130")

    ]

    cursor.executemany("""
    INSERT INTO records
    (full_name, gender, status, contact)
    VALUES (?, ?, ?, ?)
    """, sample_data)

    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_table()
    insert_sample_records()

    print("Database created successfully.")
