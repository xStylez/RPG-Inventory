import customtkinter as ctk
from items import create_item, list_items, get_item, remove_item_from_inventories, delete_item, update_item
from theme import BG_APP, BG_CARD, BG_INPUT, ACCENT, ACCENT_BRIGHT, ACCENT_HOVER, TEXT, TEXT_MUTED, SUCCESS, ERROR, BORDER, make_card, make_title, make_subtitle, make_entry, make_primary_button, make_secondary_button, make_status_label, make_textbox, make_option_menu

ITEM_TYPE = ["Weapon", "Armor", "Accessory", "Consumable"]
ITEM_RARITY = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]

class ItemsFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.items_menu_card = make_card(self)
        self.items_menu_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.items_menu_card,
            text ="Items"
            ).pack(padx=40, pady=(22, 4))

        make_subtitle(
            self.items_menu_card,
            text="Select an option to manage"
            ).pack(padx=40, pady=(0, 10))

        make_primary_button(
            self.items_menu_card,
            text= "Create Item",
            command = self.on_create_item_button_clicked
            ).pack(padx=55, pady=(10,8))

        make_primary_button(
            self.items_menu_card,
            text = "List Items",
            command = self.on_list_items_button_clicked
            ).pack(padx=55, pady=(20,8))

        make_primary_button(
            self.items_menu_card,
            text = "Search Item",
            command = self.on_search_item_button_clicked
            ).pack(padx=55, pady=(20,8))

        make_primary_button(
            self.items_menu_card,
            text = "Update Item",
            command = self.on_update_item_button_clicked
            ).pack(padx=55, pady=(20,8))

        make_primary_button(
            self.items_menu_card,
            text = "Remove Item from Inventories",
            command = self.on_remove_item_from_inventories_button_clicked
            ).pack(padx=55, pady=(20,8))
            
        make_primary_button(
            self.items_menu_card,
            text = "Delete Item",
            command = self.on_delete_item_button_clicked
            ).pack(padx=55, pady=(20,8))

        make_secondary_button(
            self.items_menu_card,
            text = "Back to Menu",
            command = self.go_to_menu
            ).pack(padx=55, pady=(20,30))

    def on_create_item_button_clicked(self):
        self.app.show_frame(self.app.create_item_frame)

    def on_list_items_button_clicked(self):
        self.app.list_items_frame.refresh_items_list()
        self.app.show_frame(self.app.list_items_frame)

    def on_search_item_button_clicked(self):
        self.app.show_frame(self.app.search_item_frame)

    def on_update_item_button_clicked(self):
        self.app.show_frame(self.app.update_item_frame)

    def on_remove_item_from_inventories_button_clicked(self):
        self.app.show_frame(self.app.remove_item_from_inventories_frame)

    def on_delete_item_button_clicked(self):
        self.app.show_frame(self.app.delete_item_frame)
    
    def go_to_menu(self):
        self.app.go_to_menu()


class CreateItemFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.create_item_card = make_card(self)
        self.create_item_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.create_item_card,
            text ="Item Creation"
            ).pack(padx=55, pady=(22, 4))

        make_subtitle(
            self.create_item_card,
            text="Please enter the item details"
            ).pack(padx=55, pady=(0, 10))

        self.item_name_entry = make_entry(
            self.create_item_card,
            placeholder_text="Name"
            )
        self.item_name_entry.pack(padx=55, pady=(10, 8))

        self.item_type_option = make_option_menu(
            self.create_item_card,
            values = ITEM_TYPE
            )
        self.item_type_option.pack(padx=55, pady=(10, 8))
        self.item_type_option.set(ITEM_TYPE[0])

        self.item_rarity_option = make_option_menu(
            self.create_item_card,
            values = ITEM_RARITY
            )
        self.item_rarity_option.pack(padx=55, pady=(10, 8))

        self.item_level_entry = make_entry(
            self.create_item_card,
            placeholder_text="Level"
            )
        self.item_level_entry.pack(padx=55, pady=(10, 8))

        self.item_value_entry = make_entry(
            self.create_item_card,
            placeholder_text="Value"
            )
        self.item_value_entry.pack(padx=55, pady=(10, 8))

        make_subtitle(
            self.create_item_card,
            text = "Description"
            ).pack(padx=55, pady=(10,0))

        self.item_description_textbox = make_textbox(
            self.create_item_card,
            width=300,
            height=75
            )
        self.item_description_textbox.pack(padx=55, pady=10)

        make_primary_button(
            self.create_item_card,
            text = "Create Item",
            command = self.on_create_item_button_clicked
            ).pack(padx=55, pady=(10,8))

        make_secondary_button(
            self.create_item_card,
            text = "Back to Items Menu",
            command = self.go_to_items
            ).pack(padx=55, pady=10)

        self.status_label = make_status_label(self.create_item_card)
        self.status_label.pack(padx=55, pady=10)

    def on_create_item_button_clicked(self):
        item_name = self.item_name_entry.get()
        item_type = self.item_type_option.get()
        item_rarity = self.item_rarity_option.get()
        item_level = self.item_level_entry.get()
        item_value = self.item_value_entry.get()
        item_description = self.item_description_textbox.get("1.0", "end-1c").strip()

        try:
            item_level = int(item_level)
            item_value = int(item_value)
        except ValueError:
            print("Please enter a valid number for level and value") # console log message
            self.status_label.configure(
                text="Please enter a valid number for level and value",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        if item_level < 1 or item_level > 99:
            print("Please enter a valid level between 1 and 99") # console log message
            self.status_label.configure(
                text="Please enter a valid level between 1 and 99",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        if item_value < 0 or item_value > 3000000:
            print("Please enter a valid value between 1 and 3000000") # console log message
            self.status_label.configure(
                text="Please enter a valid value between 1 and 3000000",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        if not item_name or not item_level or not item_value or not item_description:
            print("Please fill in all fields") # console log message
            self.status_label.configure(
                text="Please fill in all fields",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        item_created = create_item(self.app.cursor, item_name, item_type, item_rarity, item_level, item_value, item_description)
        self.app.conn.commit()

        if item_created:
            self.status_label.configure(
                text= f"Item {item_name} created successfully",
                text_color=SUCCESS
                )
            self.after(3000, self.clear_status)
            
        else:
            self.status_label.configure(
                text= f"Item {item_name} already exists",
                text_color=ERROR
                )
            self.after(3000, self.clear_status)
            

        self.item_name_entry.delete(0, "end")
        self.item_type_option.set(ITEM_TYPE[0])
        self.item_rarity_option.set(ITEM_RARITY[0])
        self.item_level_entry.delete(0, "end")
        self.item_value_entry.delete(0, "end")
        self.item_description_textbox.delete("1.0", "end")

    def clear_status(self):
        self.status_label.configure(text="")

    def go_to_items(self):
        self.app.show_frame(self.app.items_frame)

class ListItemsFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.list_items_card = make_card(self)
        self.list_items_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.list_items_card,
            text ="Items List"
            ).pack(padx=55, pady=(22, 4))

        self.items_listbox = make_textbox(self.list_items_card, width=580, height=320)
        self.items_listbox.pack(pady=10, padx=20, fill="x")
        self.items_listbox.tag_config("label", foreground=ACCENT_BRIGHT)
        self.items_listbox.tag_config("value", foreground=TEXT)
        self.items_listbox.tag_config("muted", foreground=TEXT_MUTED)

        make_secondary_button(
            self.list_items_card,
            text = "Back to Items",
            command = self.go_to_items
            ).pack(padx=55, pady=(10,15))

    def refresh_items_list(self): # refresh the items list
        self.items_listbox.delete("1.0", "end")

        items = list_items(self.app.cursor) # get the items from the database
        if not items:
            self.items_listbox.insert("end", "No items found", "muted")
            return

        for item in items:
            self.items_listbox.insert("end", "ID: ", "label")
            self.items_listbox.insert("end", f"{item[0]}  ", "value")
            self.items_listbox.insert("end", "Name: ", "label")
            self.items_listbox.insert("end", f"{item[1]}  ", "value")
            self.items_listbox.insert("end", "Type: ", "label")
            self.items_listbox.insert("end", f"{item[2]}  ", "value")
            self.items_listbox.insert("end", "Rarity: ", "label")
            self.items_listbox.insert("end", f"{item[3]}  ", "value")
            self.items_listbox.insert("end", "Level: ", "label")
            self.items_listbox.insert("end", f"{item[4]}  ", "value")
            self.items_listbox.insert("end", "Value: ", "label")
            self.items_listbox.insert("end", f"{item[5]}\n", "value")
            self.items_listbox.insert("end", "Description: ", "label")
            self.items_listbox.insert("end", f"{item[6]}\n\n", "value")



    def go_to_items(self):
        self.app.show_frame(self.app.items_frame)

class SearchItemFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.search_item_card = make_card(self)
        self.search_item_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.search_item_card,
            text ="Item Search"
            ).pack(padx=55, pady=(22, 4))

        make_subtitle(
            self.search_item_card,
            text="Please enter the item's name"
            ).pack(padx=55, pady=(0, 10))

        self.item_name_entry = make_entry(
            self.search_item_card,
            placeholder_text="Item Name"
            )
        self.item_name_entry.pack(padx=55, pady=(10, 8))

        make_primary_button(
            self.search_item_card,
            text = "Search Item",
            command = self.on_search_item_button_clicked
            ).pack(padx=55, pady=(10, 8))

        self.search_item_listbox = make_textbox(self.search_item_card, width=300, height=150)
        self.search_item_listbox.pack(pady=10, padx=20, fill="x")
        self.search_item_listbox.tag_config("label", foreground=ACCENT_BRIGHT)
        self.search_item_listbox.tag_config("value", foreground=TEXT)
        self.search_item_listbox.tag_config("muted", foreground=TEXT_MUTED)

        make_secondary_button(
            self.search_item_card,
            text = "Back to Items",
            command = self.go_to_items
            ).pack(pady=10)

        self.status_label = make_status_label(self.search_item_card, text="")
        self.status_label.pack(padx=55, pady=10)

    def go_to_items(self):
        self.app.show_frame(self.app.items_frame)

    def on_search_item_button_clicked(self):
        item_name = self.item_name_entry.get()

        self.search_item_listbox.delete("1.0", "end") # clear the search item listbox every time the button is clicked

        if not item_name: # if the item name is not entered, show an error message
            self.status_label.configure(
                text="Please enter an item name",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        item_found = get_item(self.app.cursor, item_name) # get the item from the database
        if not item_found:
            self.search_item_listbox.insert("end", "No item found", "muted")
        else:
            self.search_item_listbox.insert("end", "Name: ", "label")
            self.search_item_listbox.insert("end", f"{item_found[1]}\n", "value")
            self.search_item_listbox.insert("end", "Type: ", "label")
            self.search_item_listbox.insert("end", f"{item_found[2]}\n", "value")
            self.search_item_listbox.insert("end", "Rarity: ", "label")
            self.search_item_listbox.insert("end", f"{item_found[3]}\n", "value")
            self.search_item_listbox.insert("end", "Level: ", "label")
            self.search_item_listbox.insert("end", f"{item_found[4]}\n", "value")
            self.search_item_listbox.insert("end", "Value: ", "label")
            self.search_item_listbox.insert("end", f"{item_found[5]}\n", "value")
            self.search_item_listbox.insert("end", "Description: ", "label")
            self.search_item_listbox.insert("end", f"{item_found[6]}\n", "value")
        
    def clear_status(self):
        self.status_label.configure(text="")

class UpdateItemFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        # Select Item Frame
        self.select_item_frame = ctk.CTkFrame(self, fg_color=BG_APP)
        self.select_item_frame.pack(fill= "both", expand=True)

        self.update_select_item_card = make_card(self.select_item_frame)
        self.update_select_item_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.update_select_item_card,
            text ="Item Selection"
            ).pack(padx=55, pady=(22, 4))

        make_subtitle(
            self.update_select_item_card,
            text="Please enter the item's name"
            ).pack(padx=55, pady=(0, 10))

        self.select_item_name_entry = make_entry(
            self.update_select_item_card,
            placeholder_text="Item Name"
            )
        self.select_item_name_entry.pack(padx=55, pady=(10, 8))

        make_primary_button(
            self.update_select_item_card,
            text= "Select Item",
            command = self.on_select_update_item_button_clicked
            ).pack(padx=55, pady=(10,8))
            
        make_secondary_button(
            self.update_select_item_card,
            text = "Back to Items",
            command = self.go_to_items
            ).pack(padx=55, pady=10)

        self.select_status_label = make_status_label(self.update_select_item_card, text="")
        self.select_status_label.pack(pady=10)


        # Update Item Frame
        self.edit_item_frame = ctk.CTkFrame(self, fg_color=BG_APP)

        self.edit_item_card = make_card(self.edit_item_frame)
        self.edit_item_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.edit_item_card,
            text ="Item Update"
            ).pack(padx=55, pady=(22, 4))

        make_subtitle(
            self.edit_item_card,
            text="Please enter the item details"
            ).pack(padx=55, pady=(0, 10))

        self.original_item_name = None

        self.item_name_entry = make_entry(
            self.edit_item_card,
            placeholder_text="Item Name"
            )
        self.item_name_entry.pack(padx=55, pady=(10, 8))

        self.item_type_option = make_option_menu(
            self.edit_item_card,
            values = ITEM_TYPE
            )
        self.item_type_option.pack(padx=55, pady=(10, 8))
        self.item_type_option.set(ITEM_TYPE[0])

        self.item_rarity_option = make_option_menu(
            self.edit_item_card,
            values = ITEM_RARITY
            )
        self.item_rarity_option.pack(padx=55, pady=(10, 8))
        self.item_rarity_option.set(ITEM_RARITY[0])

        self.item_level_entry = make_entry(
            self.edit_item_card,
            placeholder_text="Item Level"
            )
        self.item_level_entry.pack(padx=55, pady=(10, 8))

        self.item_value_entry = make_entry(
            self.edit_item_card,
            placeholder_text="Item Value"
            )
        self.item_value_entry.pack(padx=55, pady=(10, 8))

        make_subtitle(
            self.edit_item_card,
            text = "Description"
            ).pack(pady=(10,0))

        self.item_description_textbox = make_textbox(
            self.edit_item_card,
            width=300,
            height=100
            )
        self.item_description_textbox.pack(padx=55, pady=(10, 8))

        make_primary_button(
            self.edit_item_card,
            text = "Update Item",
            command = self.on_update_item_button_clicked
            ).pack(padx=55, pady=(10,8))
        
        make_secondary_button(
            self.edit_item_card,
            text = "Back to Select Item",
            command = self.go_to_select_item
            ).pack(padx=55, pady=(10,8))

        self.edit_status_label = make_status_label(self.edit_item_card, text="")
        self.edit_status_label.pack(padx=55, pady=10)
       
    def on_select_update_item_button_clicked(self):
        item_name = self.select_item_name_entry.get().strip()
        if not item_name:
            self.select_status_label.configure(
                text="Please enter an item name",
                text_color="orange"
            )
            self.after(3000, self.clear_select_status)
            return
            
        
        item_selected = get_item(self.app.cursor, item_name)
        if not item_selected:
            self.select_status_label.configure(
                text= f"Item {item_name} not found",
                text_color=ERROR
            )
            self.after(3000, self.clear_select_status)
            return

        self.original_item_name = item_selected[1]

        self.item_name_entry.delete(0, "end")
        self.item_name_entry.insert(0, item_selected[1])
        self.item_type_option.set(item_selected[2])
        self.item_rarity_option.set(item_selected[3])
        self.item_level_entry.delete(0, "end")
        self.item_level_entry.insert(0, str(item_selected[4]))
        self.item_value_entry.delete(0, "end")
        self.item_value_entry.insert(0, str(item_selected[5]))
        self.item_description_textbox.delete("1.0", "end")
        self.item_description_textbox.insert("1.0", item_selected[6])

        self.select_item_frame.pack_forget()
        self.edit_item_frame.pack(fill= "both", expand=True)
            
    def go_to_select_item(self):
        self.edit_item_frame.pack_forget()
        self.select_item_frame.pack(fill= "both", expand=True)
        self.select_status_label.configure(text="")
        self.edit_status_label.configure(text="")


    def go_to_items(self):
        self.edit_item_frame.pack_forget()
        self.select_item_frame.pack(fill= "both", expand=True)
        self.select_status_label.configure(text="")
        self.edit_status_label.configure(text="")
        self.app.show_frame(self.app.items_frame)

    def clear_select_status(self):
        self.select_status_label.configure(text="")

    def clear_edit_status(self):
        self.edit_status_label.configure(text="")

    def on_update_item_button_clicked(self):
        original_item_name = self.original_item_name
        item_name = self.item_name_entry.get()
        item_type = self.item_type_option.get()
        item_rarity = self.item_rarity_option.get()
        item_level = self.item_level_entry.get()
        item_value = self.item_value_entry.get()
        item_description = self.item_description_textbox.get("1.0", "end").strip()

        try:
            item_level = int(item_level)
            item_value = int(item_value)
        except ValueError:
            print("Please enter a valid number for level and value") # console log message
            self.edit_status_label.configure(
                text="Please enter a valid number for level and value",
                text_color="orange"
                )
            self.after(3000, self.clear_edit_status)
            return

        if item_level < 1 or item_level > 99:
            print("Please enter a valid level between 1 and 99") # console log message
            self.edit_status_label.configure(
                text="Please enter a valid level between 1 and 99",
                text_color="orange"
            )
            self.after(3000, self.clear_edit_status)
            return

        if item_value < 0 or item_value > 3000000:
            print("Please enter a valid value between 1 and 3000000") # console log message
            self.edit_status_label.configure(
                text="Please enter a valid value between 1 and 3000000",
                text_color="orange"
            )
            self.after(3000, self.clear_edit_status)
            return

        if not item_name or not item_type or not item_rarity or not item_level or not item_value or not item_description:
            print("Please fill in all fields") # console log message
            self.edit_status_label.configure(
                text="Please fill in all fields",
                text_color="orange"
            )
            self.after(3000, self.clear_edit_status)
            return

        item_updated = update_item(self.app.cursor, original_item_name, item_name, item_type, item_rarity, item_level, item_value, item_description)
        self.app.conn.commit()

        if item_updated:
            self.original_item_name = item_name
            self.edit_status_label.configure(
                text= f"Item {item_name} updated successfully",
                text_color=SUCCESS
            )
            self.after(3000, self.clear_edit_status)
            return
        else:
            self.edit_status_label.configure(
                text= f"Could not update item {original_item_name} (Item may not exist or name already taken)",
                text_color=ERROR
            )
            self.after(3000, self.clear_edit_status)
            return

class RemoveItemFromInventoriesFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.remove_item_from_inventories_card = make_card(self)
        self.remove_item_from_inventories_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.remove_item_from_inventories_card,
            text ="Item Removal"
            ).pack(padx=55, pady=(22, 4))

        make_subtitle(
            self.remove_item_from_inventories_card,
            text="Please enter the item's name to remove from inventories"
            ).pack(padx=55, pady=(0, 10))

        self.remove_item_from_inventories_name_entry = make_entry(
            self.remove_item_from_inventories_card,
            placeholder_text="Item Name"
        )
        self.remove_item_from_inventories_name_entry.pack(padx=55, pady=(10, 8))

        make_primary_button(
            self.remove_item_from_inventories_card,
            text = "Remove Item From Inventories",
            command = self.on_remove_item_from_inventories_button_clicked
            ).pack(padx=55, pady=(10, 8))

        make_secondary_button(
            self.remove_item_from_inventories_card,
            text = "Back to Items",
            command = self.go_to_items
            ).pack(padx=55, pady=(10,8))

        self.remove_item_from_inventories_status_label = make_status_label(self.remove_item_from_inventories_card, text="")
        self.remove_item_from_inventories_status_label.pack(padx=55, pady=10)

    def on_remove_item_from_inventories_button_clicked(self):
        item_name = self.remove_item_from_inventories_name_entry.get().strip()

        if not item_name:
            self.remove_item_from_inventories_status_label.configure(
                text="Please enter an item name",
                text_color="orange"
            )
            self.after(3000, self.clear_remove_item_from_inventories_status)
            return

        item_selected_to_remove = get_item(self.app.cursor, item_name)

        if not item_selected_to_remove:
            self.remove_item_from_inventories_status_label.configure(
                text= f"Item {item_name} not found in any inventories",
                text_color=ERROR
            )
            self.after(3000, self.clear_remove_item_from_inventories_status)
            return

        item_to_remove_id = item_selected_to_remove[0] # get the id of the item to remove
        item_to_remove_name = item_selected_to_remove[1] # get the name of the item to remove

        item_removed, error_message = remove_item_from_inventories(self.app.cursor, item_to_remove_id, item_to_remove_name)
        self.app.conn.commit()

        if error_message is None and item_removed is True:
            self.remove_item_from_inventories_status_label.configure(
                text= f"Item {item_to_remove_name} has been removed from inventories successfully",
                text_color=SUCCESS
            )
            self.after(3000, self.clear_remove_item_from_inventories_status)
            return

        elif error_message == "item not found" and item_removed is False:
            self.remove_item_from_inventories_status_label.configure(
                text= f"Item {item_to_remove_name} not found",
                text_color=ERROR
            )
            self.after(3000, self.clear_remove_item_from_inventories_status)
            return

        self.remove_item_from_inventories_name_entry.delete(0, "end")

    def clear_remove_item_from_inventories_status(self):
        self.remove_item_from_inventories_status_label.configure(text="")

    def go_to_items(self):
        self.app.show_frame(self.app.items_frame)

class DeleteItemFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.delete_item_card = make_card(self)
        self.delete_item_card.place(relx=0.5, rely=0.5, anchor="center")


        make_title(
            self.delete_item_card,
            text ="Delete Item"
            ).pack(padx=55, pady=(22, 4))
        
        make_subtitle(
            self.delete_item_card,
            text="Please enter the item's name to delete"
            ).pack(padx=55, pady=(0, 10))

        self.delete_item_name_entry = make_entry(
            self.delete_item_card,
            placeholder_text="Item Name"
            )
        self.delete_item_name_entry.pack(pady=10)
            
        make_primary_button(
            self.delete_item_card,
            text = "Delete Item",
            command = self.on_delete_item_button_clicked
            ).pack(padx=55, pady=(10, 8))

        make_secondary_button(
            self.delete_item_card,
            text = "Back to Items",
            command = self.go_to_items
            ).pack(padx=55, pady=(10,8))

        self.delete_status_label = make_status_label(self.delete_item_card, text="")
        self.delete_status_label.pack(padx=55, pady=10)

    def on_delete_item_button_clicked(self):
        item_selected = self.delete_item_name_entry.get().strip() #gets the name of the item we want to delete

        if not item_selected:
            self.delete_status_label.configure(
                text="Please enter an item name",
                text_color="orange"
            )
            self.after(3000, self.clear_delete_status)
            return

        item_deleted, error_message = delete_item(self.app.cursor, item_selected)
        self.app.conn.commit()

        if error_message is None:
            self.delete_status_label.configure(
                text = f"item {item_selected} has been deleted successfully",
                text_color=SUCCESS
            )
            self.after (3000, self.clear_delete_status)
            return
        elif error_message == "item not found":
            self.delete_status_label.configure(
                text = f"Item {item_selected} not found",
                text_color=ERROR
            )
            self.after(3000, self.clear_delete_status)
            return

        else:
            self.delete_status_label.configure(
                text = f"Cannot delete {item_selected}. It is still being used in inventory.",
                text_color=ERROR
            )
            self.after(3000, self.clear_delete_status)
            return

    def clear_delete_status(self):
        self.delete_status_label.configure(text="")

    def go_to_items(self):
        self.app.show_frame(self.app.items_frame)