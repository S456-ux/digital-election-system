import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Create voters table
cur.execute("""
CREATE TABLE IF NOT EXISTS voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# Create candidates table
cur.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    votes INTEGER DEFAULT 0
)
""")

# Insert candidates
cur.execute("INSERT INTO candidates (name, votes) VALUES ('A', 0)")
cur.execute("INSERT INTO candidates (name, votes) VALUES ('B', 0)")

conn.commit()
conn.close()

print("Database initialized!")