# RPG Inventory Manager (GUI)

A desktop RPG inventory manager built with **Python**, **CustomTkinter**, and **SQLite**. Manage characters, items, and per-character inventories through a dark-themed graphical interface.

This is the GUI version.

## Features

- **Login screen** — simple hardcoded demo login (not real user accounts)
- **Characters** — create, list, search, and level up
- **Items** — create, list, search, update, delete, and clear an item from all inventories
- **Inventory** — add/remove items, view a character’s bag, check item quantity
- **Themed UI** — shared colors and widget helpers in `theme.py`

## Download (Windows) — easiest way

You do **not** need Python or the source code to try the app.

1. Go to **[Releases](https://github.com/xStylez/RPG-Inventory/releases)**
2. Open the latest release (e.g. **v1.0.0**)
3. Download **`dist.zip`** (under Assets)
4. Unzip the folder
5. Double-click **`RPGInventory.exe`**

Windows may warn about an unknown publisher — choose **More info** → **Run anyway** if you trust the build.

### Demo login

| Username | Password   |
| -------- | ---------- |
| `admin`  | `admin123` |

On first run the app creates a local `rpg_inventory.db` next to the executable (your data stays on your PC).

Full day-to-day usage notes: [MANUAL.md](MANUAL.md).

---

## Run from source (developers)

Use this if you want to change the code or run without the `.exe`.

### Requirements

- Python 3.10+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

```bash
pip install customtkinter
```

### How to run

From this folder:

```bash
python main.py
```

---

## Project structure

```text
project_rpg_inventory_gui/
├── main.py                 # App window, login, menu, screen switching
├── theme.py                # Colors and UI helper widgets
├── db.py                   # SQLite connection + table setup
├── characters.py           # Character database operations
├── characters_screen.py    # Character screens
├── items.py                # Item database operations
├── items_screen.py         # Item screens
├── inventory.py            # Inventory database operations
├── inventory_screen.py     # Inventory screens
├── README.md               # This file
├── MANUAL.md               # User / feature guide
└── .gitignore
```

## Quick demo walkthrough

1. Log in with `admin` / `admin123`
2. **Characters** → create a character (e.g. `Hero`, Warrior)
3. **Items** → create an item (e.g. `Iron Sword`, Weapon, Common)
4. **Inventory** → add `Iron Sword` to `Hero` with quantity `2`
5. Add the same item again with quantity `3` → view inventory (quantity should be **5**)
6. Remove some or all → view again

## Design notes

- One SQLite connection is opened in `App` and shared with screens via `self.app.cursor` / `self.app.conn`
- Screens handle user messages; backend helpers talk to the database
- Adding an item that already exists in a bag **increases quantity** instead of creating a duplicate row
- Deleting an item is blocked while it still appears in any inventory (clear it from inventories first)
- Skillcores exist in the database schema for future work but are **not** exposed in the GUI yet
