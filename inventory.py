from items import get_item
from characters import get_character

def add_item_to_inventory(cursor, character_name, item_name, quantity):
    item = get_item(cursor, item_name)
    if item is None:
        print(f"Item {item_name} not found cannot add to inventory")
        return False

    character = get_character(cursor, character_name)
    if character is None:
        print(f"Character {character_name} not found")
        return False

    character_id = character[0]
    item_id = item[0]

    cursor.execute(
        "SELECT id FROM inventory WHERE character_id = ? AND item_id = ?",
        (character_id, item_id),
    )
    existing = cursor.fetchone()
    if existing:
        cursor.execute(
            "UPDATE inventory SET quantity = quantity + ? WHERE id = ?",
            (quantity, existing[0]),
        )
        print(f"Item {item_name} added to {character_name}'s inventory")
        return True
    else:
        cursor.execute(
            "INSERT INTO inventory(character_id, item_id, quantity) VALUES (?, ?, ?)",
            (character_id, item_id, quantity),
        )
        print(f"Item {item_name} added to {character_name}'s inventory")
        return True

def remove_item_from_inventory(cursor, character_name, item_name, quantity):
    item = get_item(cursor, item_name)
    if item is None:
        print(f"Item {item_name} not found, cannot remove from inventory")
        return False, "item not found"

    character = get_character(cursor, character_name)
    if character is None:
        print(f"Character {character_name} not found")
        return False, "character not found"

    character_id = character[0]
    item_id = item[0]

    quantity_total, error_message = get_item_quantity(cursor, character_name, item_name)

    if quantity_total == 0:
        print(f"Item {item_name} not found in {character_name}'s inventory") #debugging
        return False, "not in inventory"

    if quantity_total < quantity:
        print(f"Item {item_name} exists only {quantity_total} time(s)in {character_name}'s inventory. Cannot remove {quantity}") #debugging
        return False, "not enough items in inventory"

    elif quantity_total == quantity:
        cursor.execute ("DELETE FROM inventory WHERE character_id =? AND item_id =? AND quantity >= ?", (character_id, item_id, quantity))
        print(f"Item {item_name} removed from {character_name}'s inventory") #debugging
        return True, None
        
    else:
        cursor.execute("UPDATE inventory SET quantity =? WHERE character_id =? AND item_id=?", (quantity_total - quantity, character_id, item_id))
        print(f"Item {item_name} removed {quantity} time(s) from {character_name}'s inventory") #debugging
        return True, None

def get_inventory(cursor, character_name):
    character = get_character(cursor, character_name)
    if character is None:
        print(f"Character {character_name} not found") #debugging
        return None, "character not found"

    character_id = character[0]

    cursor.execute("""
        SELECT items.name AS item_name, inventory.quantity AS quantity 
        FROM inventory
        JOIN items ON inventory.item_id = items.id 
        WHERE inventory.character_id =?
        """, (character_id,))

    inventory = cursor.fetchall()
    if not inventory:
        print(f"No items in {character_name}'s inventory") #debugging
        return None, "no items in inventory"
    else:
        for item in inventory:
            print(f"Item: {item[0]} Quantity: {item[1]}") #debugging
        return inventory, "items in inventory"


def get_item_quantity(cursor, character_name, item_name):
    character = get_character(cursor, character_name)
    if character is None:
        return None, "character not found"
    character_id = character[0]
    
    item = get_item(cursor, item_name)
    if item is None:
        return None, "item not found"
    item_id = item[0]

    cursor.execute("SELECT quantity FROM inventory WHERE character_id =? AND item_id =?", (character_id, item_id))
    quantity = cursor.fetchone()
    if quantity is None:
        return 0, "not_in_inventory"
    else:
        return quantity[0], None
