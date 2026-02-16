import sqlite3

conn = sqlite3.connect("contacts.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT
)
""")

conn.commit()
conn.close()

print("Database created")