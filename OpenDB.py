import sqlite3

conn = sqlite3.connect("uptime_monitor/db.sqlite3")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

cursor.execute("SELECT * FROM monitor_monitoredurl")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()