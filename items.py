import sqlite3

def create_item(cursor, name, item_type, rarity, level, value, description):
    try:
        cursor.execute("INSERT INTO items(name, item_type, rarity, level, value, description) VALUES (?, ?, ?, ?, ?, ?)", (name, item_type, rarity, level, value, description))
        print(f"Item {name} created successfully") # console log message
        return True
    except sqlite3.IntegrityError:
        print(f"Item {name} already exists") # console log message
        return False

def list_items(cursor):
    cursor.execute("SELECT * FROM items")
    items_search = cursor.fetchall()
    return items_search

def get_item(cursor, item_name):
    cursor.execute("SELECT * FROM items where name =?", (item_name,))
    item_check = cursor.fetchone()
    if not item_check:
        return
    else:
        return item_check

def remove_item_from_inventories(cursor, item_id, item_name):
        cursor.execute("DELETE FROM inventory where item_id =?", (item_id,))
        if cursor.rowcount == 0:
            print(f"Item {item_name} not found") #debugging
            return False, "item not found"

        print(f"Item {item_name} has been removed from inventories successfully")
        return True, None

def delete_item(cursor, item_name):
    try:
        cursor.execute("DELETE FROM items where name =?", (item_name,))

        if cursor.rowcount == 0:
            print(f"Item {item_name} not found") #debugging
            return False, "item not found"

        print(f"Item {item_name} deleted successfully")
        return True, None

    except sqlite3.IntegrityError:
        print(f"Cannot delete {item_name}. It is still being used in inventory or has a skillcore attached to it.") #debugging
        return False, "item still in character's inventory"

def update_item(cursor, original_item_name, item_name, item_type, item_rarity, item_level, item_value, item_description):
    try:
        cursor.execute("UPDATE items set name =?, item_type =?, rarity =?, level =?, value =?, description =? where name =?", (item_name, item_type, item_rarity, item_level, item_value, item_description, original_item_name))
        print(f"Item {item_name} updated successfully")
        return True
    except sqlite3.IntegrityError:
        print(f"Item {item_name} not found or cannot be updated")
        return False

"""  Old update item functions - functional but not used in the GUI - could work if i need to change the update method 

def update_item_name(cursor, item_name, new_item_name):
    cursor.execute("UPDATE items set name =? where name =?", (new_item_name, item_name))
    print(f"Item {item_name} updated to {new_item_name}")

def update_item_type(cursor, item_name, new_item_type):
    cursor.execute("UPDATE items set item_type =? where name =?", (new_item_type, item_name))
    print(f"Item {item_name} updated to {new_item_type}")

def update_item_rarity(cursor, item_name, new_rarity):
    cursor.execute("UPDATE items set rarity =? where name =?", (new_rarity, item_name))
    print(f"Item {item_name} updated to {new_rarity}")

def update_item_level(cursor, item_name, new_level):
    cursor.execute("UPDATE items set level =? where name =?", (new_level, item_name))
    print(f"Item {item_name} updated to {new_level}")

def update_item_value(cursor, item_name, new_value):
    cursor.execute("UPDATE items set value =? where name =?", (new_value, item_name))
    print(f"Item {item_name} updated to {new_value}")

def update_item_description(cursor, item_name, new_description):
    cursor.execute("UPDATE items set description =? where name =?", (new_description, item_name))
    print(f"Item {item_name} updated to {new_description}")
"""


# skillcores not implemented yet - Future work
def add_skillcore(cursor, item_name):
    item = get_item_with_skillcore(cursor, item_name)
    if item is None:
        return 
    
    if item[5] != "Legendary" or item[4] != "Weapon" or item[2] is not None:
        print(f"Item {item_name} is not a Legendary Weapon or already has a skillcore, cannot add a new skillcore")
        return

    item_id = item[0]   # first column is id

    skill_name = input("Enter the skillcore's name: ")
    skill_description = input("Enter the skillcore's description: ")

    cursor.execute(
        "INSERT INTO skillcore (item_id, skill_name, skill_description) VALUES (?, ?, ?)",
        (item_id, skill_name, skill_description)
    )
    print(f"Skillcore '{skill_name}' added to {item_name}")

 # skillcores not implemented yet - Future work
def get_item_with_skillcore(cursor, item_name):
    cursor.execute("SELECT items.id, items.name, skillcore.skill_name, skillcore.skill_description,items.item_type, items.rarity, items.level, items.value, items.description FROM items LEFT JOIN skillcore ON items.id = skillcore.item_id WHERE items.name =?", (item_name,))
    item_with_skillcore = cursor.fetchone()
    if not item_with_skillcore:
        return
    else:
        return item_with_skillcore
