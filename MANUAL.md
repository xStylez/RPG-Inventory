# RPG Inventory Manager — Manual

How to use the GUI app day to day. For install and project layout, see [README.md](README.md).

---

## Starting the app

1. Open a terminal in this folder (`project_rpg_inventory_gui`).
2. Run:

   ```bash
   python main.py
   ```

3. The login screen appears.

### Login

| Field    | Demo value  |
|----------|-------------|
| Username | `admin`     |
| Password | `admin123`  |

- Empty fields → warning to fill them in  
- Wrong credentials → error message  
- Success → brief confirmation, then the main **Menu**

> This login is for practice only. There are no real user accounts yet.

**Logout** (from the Menu) returns you to the login screen.

---

## Main menu

After login you can open:

| Button        | What it opens                                      |
|---------------|----------------------------------------------------|
| **Characters** | Character management                               |
| **Items**      | Item catalog management                            |
| **Inventory**  | Give items to characters / inspect bags            |
| **Logout**     | Back to login                                      |

Use **Back** on each screen to return to the previous menu.

---

## Characters

### Create character

1. Enter a **unique** name.
2. Choose a class:
   - Warrior  
   - Mage  
   - Steelheart  
   - Assassin  
   - Druid  
3. A short class description is shown under the dropdown.
4. Confirm create.

New characters start at **level 1**. Duplicate names are rejected.

### List characters

Shows every character: name, class, and level.

### Search character

Enter an exact name. If found, details are shown; if not, you get a clear status message.

### Level up

Enter the character’s name and confirm. Level increases by **1**. Unknown names show an error.

---

## Items

### Create item

Fill in:

| Field         | Notes                                                |
|---------------|------------------------------------------------------|
| Name          | Must be unique                                       |
| Type          | Weapon, Armor, Accessory, Consumable                 |
| Rarity        | Common, Uncommon, Rare, Epic, Legendary              |
| Level         | Integer                                              |
| Value         | Integer (in-game worth)                              |
| Description   | Free text                                            |

### List / Search

- **List** shows all items in the catalog.  
- **Search** looks up one item by exact name.

### Update item

1. Enter the current item name and load it.
2. Edit the fields (including renaming).
3. Save.

The update targets the item you originally loaded, then keeps using the new name if you renamed it.

### Clear from all inventories

Removes that item from **every** character’s bag (sets those inventory rows gone). Useful before deleting an item that is still in use.

### Delete item

Deletes the item from the catalog.

- If the item is still in any inventory → delete is **blocked**. Clear it from inventories first (or remove per character under Inventory).
- If the name does not exist → not-found message.

---

## Inventory

You must already have at least one character and one item.

### Add item to inventory

1. Character name  
2. Item name  
3. Quantity (positive number)

If that character already has the item, quantity is **added** to the existing stack.

### Remove item from inventory

Same fields. Quantity is reduced; if it reaches zero, the row is removed. You cannot remove more than the character currently has.

### View character inventory

Enter a character name to see all items and quantities in their bag.

### View item quantity

Enter character name + item name to see how many of that item they hold.

---

## Suggested practice flow

1. Create character `Hero` (Warrior).  
2. Create item `Iron Sword` (Weapon / Common / level 1 / value 50).  
3. Add `Iron Sword` × 2 to `Hero`.  
4. Add `Iron Sword` × 3 again → bag should show **5**.  
5. View inventory / view quantity to confirm.  
6. Remove `3` → quantity **2**.  
7. Try delete item while it is still in the bag → should fail.  
8. Clear from all inventories (or remove the rest), then delete successfully.  
9. Level up `Hero` and search again.

---

## Data and files

| File / thing           | Purpose                                      |
|------------------------|----------------------------------------------|
| `rpg_inventory.db`     | Local SQLite database (created on first run) |
| `.gitignore`           | Keeps `.db`, `__pycache__`, editor junk out of git |

Closing the window ends the session. Data already committed to the database stays for the next run.

---

## Limitations / future ideas

- Login is hardcoded (`admin` / `admin123`) — no multi-user accounts yet  
- Skillcores are prepared in the database schema but **not** available in the GUI  
- Names for search/create are exact matches (no fuzzy search)

---

## Troubleshooting

| Problem                         | What to try                                      |
|---------------------------------|--------------------------------------------------|
| `ModuleNotFoundError: customtkinter` | Run `pip install customtkinter`            |
| Window opens but DB seems empty | Normal on first run — create characters/items first |
| Cannot delete an item           | Remove it from inventories first                 |
| Login always fails              | Use exactly `admin` / `admin123` (case-sensitive)|
| Wrong folder                    | Run `python main.py` from `project_rpg_inventory_gui` so the DB is created next to the code |
