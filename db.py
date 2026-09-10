import sqlite3

def get_connection():
    return sqlite3.connect("rpg_inventory.db")


def setup_database():

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            level INTEGER NOT NULL,
            UNIQUE (name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            item_type TEXT NOT NULL,
            rarity TEXT NOT NULL,
            level INTEGER NOT NULL,
            value INTEGER NOT NULL,
            description TEXT NOT NULL,
            UNIQUE (name)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (character_id) REFERENCES characters(id),
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    """)

    # skillcores not implemented yet - Future work
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skillcore (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        skill_name TEXT NOT NULL,
        skill_description TEXT NOT NULL,
        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
        UNIQUE (item_id)
    )
    """)

    connection.commit()
    connection.close()