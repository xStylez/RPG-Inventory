import sqlite3

def create_character(cursor, name, class_name):
    try:
        cursor.execute("INSERT INTO characters (name, class_name, level) VALUES (?, ?, 1)", (name, class_name,))
        print(f"Character {name} created successfully")
        return True
    except sqlite3.IntegrityError:
        print(f"Character {name} already exists")
        return False

def list_characters(cursor):
    cursor.execute("SELECT * FROM characters")
    characters_check = cursor.fetchall()
    if not characters_check:
        print("No characters found")
        return []
    else:
        return characters_check

def get_character(cursor,character_name):
    cursor.execute ("SELECT * FROM characters WHERE name =?", (character_name,))
    character_check = cursor.fetchone()
    if not character_check:
        print(f"Character {character_name} not found")
        return None
    else:
        return character_check

def character_level_up(cursor, character_name):
    cursor.execute("SELECT level FROM characters WHERE name =?", (character_name,))
    character_level = cursor.fetchone()
    if not character_level:
        print(f"Character {character_name} not found")
        return
    else:
        cursor.execute("UPDATE characters SET level = level + 1 WHERE name =?", (character_name,))
        print(f"{character_name} leveled up to level {character_level[0] + 1}")
        return character_level[0] + 1