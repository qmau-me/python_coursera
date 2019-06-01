import re
import sqlite3

conn = sqlite3.connect('python.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('CREATE TABLE Counts (org Text, count INTEGER)')

file = open('mbox.txt')
for line in file:
    org = re.findall('From\S.+@(\S+)', line)
    if len(org) > 0:
        cur.execute('SELECT count FROM Counts WHERE org = ?', (org[0],))
        row = cur.fetchone()
        if row is None:
                cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org[0],))
        else:
                cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org[0],))
        conn.commit()

rows = cur.execute('SELECT org,count FROM Counts ORDER BY count DESC LIMIT 5')

for row in rows:
        print(str(row[0]), row[1])

cur.close()