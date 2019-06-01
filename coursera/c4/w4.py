import json
import sqlite3

conn = sqlite3.connect('w4.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

file = open('roster_data.json').read()
data = json.loads(file)
for info in data:
    if (len(info) < 3): continue
    print(info)

    user = info[0]
    course = info[1]
    role = info[2]

    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (user,))
    row = cur.execute('SELECT id FROM User WHERE name = ?', (user,))
    user_id = row.fetchone()[0]
    print(user_id)

    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (course,))
    row = cur.execute('SELECT id FROM Course WHERE title = ?', (course,))
    course_id = row.fetchone()[0]
    print(course_id)


    cur.execute('''INSERT OR REPLACE INTO Member (user_id, course_id, role)
        VALUES( ?, ?, ? )''' , (user_id, course_id, role))
    conn.commit

print(cur.execute(
'''SELECT hex(User.name || Course.title || Member.role ) AS X FROM
    User JOIN Member JOIN Course
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X
''').fetchone()[0])

