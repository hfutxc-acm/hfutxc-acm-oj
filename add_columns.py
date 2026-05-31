import sqlite3

conn = sqlite3.connect('/home/ikun/PycharmProjects/hfutxc-acm-oj/data/oj.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE submissions ADD COLUMN time_ms INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    print("Column time_ms already exists")

try:
    cursor.execute("ALTER TABLE submissions ADD COLUMN memory_kb INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    print("Column memory_kb already exists")

conn.commit()
conn.close()
print("Done!")
