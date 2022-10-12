import sqlite3


conn = sqlite3.connect('db.sqlite')
cur = conn.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS chats(
    chat_id INT PRIMARY KEY,
    first_name TEXT, 
    last_name TEXT,
    role_id INT);"""
)
cur.execute(
    """CREATE TABLE IF NOT EXISTS roles(
    role_id INT PRIMARY KEY,
    caption TEXT);"""
)
cur.execute(
    """CREATE TABLE IF NOT EXISTS checklist_points(
    point_id INT PRIMARY KEY,
    text TEXT,
    role_id INT);"""
)
cur.execute(
    """CREATE TABLE IF NOT EXISTS checklists(
    checklist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INT,
    points_done_json TEXT,
    creation_datetime DATETIME,
    update_datetime DATETIME);"""
)
conn.commit()
