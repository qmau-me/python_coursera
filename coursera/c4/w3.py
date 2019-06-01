import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('w3.sqlite')
cur = conn.cursor()

# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

file = open('Library.xml')
data = ET.parse(file)
tracks = data.findall('./dict/dict/dict')
print("Dict count: ", len(tracks))
for track in tracks:
    if (lookup(track, "Track ID") == None): continue
    name = lookup(track, 'Name')
    artist = lookup(track, 'Artist')
    album = lookup(track, 'Album')
    count = lookup(track, 'Play Count')
    rating = lookup(track, 'Rating')
    length = lookup(track, 'Total Time')
    genre = lookup(track, 'Genre')

    if (name is None or artist is None or album is None or genre is None): continue

    print(name, artist, album, count, rating, length)

    cur.execute('''
        INSERT OR IGNORE INTO Artist (name)
            VALUES( ?)
    ''' , (artist,))
    row = cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artist_id = row.fetchone()[0]

    cur.execute('''
        INSERT OR IGNORE INTO Album (title, artist_id)
            VALUES ( ?, ?)''' , (album, artist_id))
    row = cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = row.fetchone()[0]

    cur.execute('''
        INSERT OR IGNORE INTO Genre (name)
            VALUES( ? )
    ''' , (genre,))
    row = cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genre_id = row.fetchone()[0]

    cur.execute('''
        INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count)
            VALUES ( ?, ?, ?, ?, ?, ? )''',
        (name, album_id, genre_id, length, rating, count))
conn.commit()