
import sqlite3
import os

DB_PATH = os.path.join("data", "coachai.db")

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Oyuncu tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            number INTEGER,
            position TEXT,
            image_path TEXT
        )
    ''')

    # Sadeleştirilmiş stats tablosu
    c.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            date TEXT,
            minutes INTEGER,
            points INTEGER,
            assists INTEGER,
            rebounds INTEGER,
            steals INTEGER,
            blocks INTEGER,
            FOREIGN KEY(player_id) REFERENCES players(id)
        )
    ''')

    conn.commit()
    conn.close()

def add_player(name, number, position, image_path=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO players (name, number, position, image_path) VALUES (?, ?, ?, ?)',
        (name, number, position, image_path)
    )
    conn.commit()
    conn.close()

def insert_stat(player_id, stat_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO stats (
            player_id, date, minutes, points,
            assists, rebounds, steals, blocks
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        player_id,
        stat_data.get("date"),
        stat_data.get("minutes", 0),
        stat_data.get("points", 0),
        stat_data.get("assists", 0),
        stat_data.get("rebounds", 0),
        stat_data.get("steals", 0),
        stat_data.get("blocks", 0)
    ))
    conn.commit()
    conn.close()

def get_all_players():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM players')
    result = c.fetchall()
    conn.close()
    return result

def get_player_stats(player_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM stats WHERE player_id = ?', (player_id,))
    result = c.fetchall()
    conn.close()
    return result
