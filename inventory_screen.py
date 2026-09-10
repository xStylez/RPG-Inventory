import customtkinter as ctk
from inventory import add_item_to_inventory, remove_item_from_inventory, get_inventory, get_item_quantity
from theme import BG_APP, BG_CARD, BG_INPUT, ACCENT, ACCENT_BRIGHT, ACCENT_HOVER, TEXT, TEXT_MUTED, SUCCESS, ERROR, BORDER, make_card, make_title, make_subtitle, make_entry, make_primary_button, make_secondary_button, make_status_label, make_textbox, make_option_menu


class InventoryFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.inventory_menu_card = make_card(self)
        self.inventory_menu_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.inventory_menu_card,
            "Inventory"
            ).pack(padx=40, pady=(22, 4))

        make_subtitle(
            self.inventory_menu_card,
            "Select an option to manage inventory"
            ).pack(padx=40, pady=(0, 10))

        make_primary_button(
            self.inventory_menu_card,
            "Add Item to Inventory",
            command = self.on_add_item_to_inventory
        ).pack(padx=55, pady=(10,8))

        make_primary_button(
            self.inventory_menu_card,
            "Remove Item from Inventory",
            command = self.on_remove_item_from_inventory
        ).pack(padx=55, pady=(20,8))
    
        make_primary_button(
            self.inventory_menu_card,
            text = "View Character Inventory",
            command = self.on_view_character_inventory
        ).pack(padx=55, pady=(20,8))

        make_primary_button(
            self.inventory_menu_card,
            text = "View Item Quantity",
            command = self.on_view_item_quantity
        ).pack(padx=55, pady=(20,8))

        make_secondary_button(
            self.inventory_menu_card,
            text = "Back to Main Menu",
            command = self.go_to_menu
        ).pack(padx=55, pady=(20,30))

    def on_add_item_to_inventory(self):
        self.app.show_frame(self.app.add_item_to_inventory_frame)
    
    def on_remove_item_from_inventory(self):
        self.app.show_frame(self.app.remove_item_from_inventory_frame)
    
    def on_view_character_inventory(self):
        self.app.show_frame(self.app.view_character_inventory_frame)
    
    def on_view_item_quantity(self):
        self.app.show_frame(self.app.view_item_quantity_frame)

    def go_to_menu(self):
        self.app.show_frame(self.app.menu_frame)


class AddItemToInventoryFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.add_item_to_inventory_card = make_card(self)
        self.add_item_to_inventory_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.add_item_to_inventory_card,
            "Add Item to Inventory"
        ).pack(padx=55, pady=(22, 4))

        make_subtitle(
            self.add_item_to_inventory_card,
            "Fill in the fields below"
        ).pack(padx=55, pady=(0, 10))

        self.inventory_character_selection_entry = make_entry(
            self.add_item_to_inventory_card,
            placeholder_text = "Character's name"
        )
        self.inventory_character_selection_entry.pack(padx=55, pady=(10,8))

        self.inventory_item_selection_entry = make_entry(
            self.add_item_to_inventory_card,
            placeholder_text = "Item's name"
        )
        self.inventory_item_selection_entry.pack(padx=55, pady=(10,8))

        self.inventory_quantity_selection_entry = make_entry(
            self.add_item_to_inventory_card,
            placeholder_text = "Quantity"
        )
        self.inventory_quantity_selection_entry.pack(padx=55, pady=(10,8))

        make_primary_button(
            self.add_item_to_inventory_card,
            text = "Add to Inventory",
            command = self.on_add_item_to_inventory
        ).pack(padx=55, pady=(10,8))

        make_secondary_button(
            self.add_item_to_inventory_card,
            text = "Back to Inventory Management",
            command = self.go_to_inventory_management
        ).pack(padx=55, pady=(10,15))

        self.add_item_to_inventory_status_label = make_status_label(self.add_item_to_inventory_card, wraplength=280, justify="center")
        self.add_item_to_inventory_status_label.pack(padx=55, pady=(10,8))

    def on_add_item_to_inventory(self):
        selected_character_name = self.inventory_character_selection_entry.get().strip()
        selected_item_name = self.inventory_item_selection_entry.get().strip()
        try:
            selected_quantity = int(self.inventory_quantity_selection_entry.get())
        except ValueError:
            self.add_item_to_inventory_status_label.configure(
                text="Please enter a valid quantity",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        if not selected_character_name or not selected_item_name or not selected_quantity:
            self.add_item_to_inventory_status_label.configure(
                text="Please enter a character name, item name, and quantity",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        if selected_quantity < 1:
            self.add_item_to_inventory_status_label.configure(
                text="Please enter a quantity greater than 0",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        item_added = add_item_to_inventory(self.app.cursor, selected_character_name, selected_item_name, selected_quantity)

        if not item_added:
            self.add_item_to_inventory_status_label.configure(
                text = f"Item: {selected_item_name} or Character: {selected_character_name} not found",
                text_color=ERROR
            )
            self.after(3000, self.clear_status)
            return

        else:
            if selected_quantity > 1:
                self.add_item_to_inventory_status_label.configure(
                    text= f"{selected_quantity} {selected_item_name}'s have been added to {selected_character_name}'s inventory successfully",
                    text_color=SUCCESS
                )
                self.app.conn.commit()
                self.after(3000, self.clear_status)
                return
            elif selected_quantity == 1:
                self.add_item_to_inventory_status_label.configure(
                    text= f"{selected_quantity} {selected_item_name} has been added to {selected_character_name}'s inventory successfully",
                    text_color=SUCCESS
                )
                self.app.conn.commit()
                self.after(3000, self.clear_status)
                return

    def clear_status(self):
        self.add_item_to_inventory_status_label.configure(text="")

    def go_to_inventory_management(self):
        self.app.show_frame(self.app.inventory_frame)

class RemoveItemFromInventoryFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app
        
        self.remove_item_from_inventory_card = make_card(self)
        self.remove_item_from_inventory_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.remove_item_from_inventory_card,
            "Remove Item from Inventory"
        ).pack(padx=55, pady=(22, 4))

        make_subtitle(
            self.remove_item_from_inventory_card,
            "Fill in the fields below"
        ).pack(padx=55, pady=(0, 10))

        self.inventory_character_selection_entry = make_entry(
            self.remove_item_from_inventory_card,
            placeholder_text = "Character's name"
        )
        self.inventory_character_selection_entry.pack(padx=55, pady=(10,8))

        self.inventory_item_selection_entry = make_entry(
            self.remove_item_from_inventory_card,
            placeholder_text = "Item's name"
        )
        self.inventory_item_selection_entry.pack(padx=55, pady=(10,8))

        self.inventory_quantity_selection_entry = make_entry(
            self.remove_item_from_inventory_card,
            placeholder_text = "Quantity"
        )
        self.inventory_quantity_selection_entry.pack(padx=55, pady=(10,8))

        make_primary_button(
            self.remove_item_from_inventory_card,
            text = "Remove from Inventory",
            command = self.on_remove_item_from_inventory
        ).pack(padx=55, pady=(10,8))

        make_secondary_button(
            self.remove_item_from_inventory_card,
            text = "Back to Inventory Management",
            command = self.go_to_inventory_management
        ).pack(padx=55, pady=(10,15))
        
        self.remove_item_from_inventory_status_label = make_status_label(self.remove_item_from_inventory_card)
        self.remove_item_from_inventory_status_label.pack(padx=55, pady=(10,8))

    def on_remove_item_from_inventory(self):
        selected_character_name = self.inventory_character_selection_entry.get().strip()
        selected_item_name = self.inventory_item_selection_entry.get().strip()
        try:
            selected_quantity = int(self.inventory_quantity_selection_entry.get())
        except ValueError:
            self.remove_item_from_inventory_status_label.configure(
                text="Please enter a valid quantity",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        if selected_quantity < 1:
            self.remove_item_from_inventory_status_label.configure(
                text="Please enter a quantity greater than 0",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        if not selected_character_name or not selected_item_name or not selected_quantity:
            self.remove_item_from_inventory_status_label.configure(
                text="Please fill in all fields",
                text_color="orange"
            )   
            self.after(3000, self.clear_status)
            return

        item_removed, error_message = remove_item_from_inventory(self.app.cursor, selected_character_name, selected_item_name, selected_quantity)

        if error_message == "item not found":
            self.remove_item_from_inventory_status_label.configure(
                text = f"Item: {selected_item_name} not found",
                text_color=ERROR
            )
            self.after(3000, self.clear_status)
            return

        elif error_message == "character not found":
            self.remove_item_from_inventory_status_label.configure(
                text = f"Character: {selected_character_name} not found",
                text_color=ERROR
            )
            self.after(3000, self.clear_status)
            return
            
        elif error_message == "not enough items in inventory":
            self.remove_item_from_inventory_status_label.configure(
                text = f"Not enough items in {selected_character_name}'s inventory",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        elif error_message == "not in inventory":
            self.remove_item_from_inventory_status_label.configure(
                text = f"No such item in {selected_character_name}'s inventory",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return
        else:
            if selected_quantity > 1 and error_message is None:
                self.remove_item_from_inventory_status_label.configure(
                    text = f"{selected_quantity} {selected_item_name}'s have been removed from\n"
                    f"{selected_character_name}'s inventory successfully",
                    text_color=SUCCESS
                )
                self.app.conn.commit()
                self.after(3000, self.clear_status)
                return
            elif selected_quantity == 1 and error_message is None:
                self.remove_item_from_inventory_status_label.configure(
                    text = f"{selected_quantity} {selected_item_name} has been removed from\n"
                    f"{selected_character_name}'s inventory successfully",
                    text_color=SUCCESS
                )
                self.app.conn.commit()
                self.after(3000, self.clear_status)
                return

    def clear_status(self):
        self.remove_item_from_inventory_status_label.configure(text="")

    def go_to_inventory_management(self):
        self.app.show_frame(self.app.inventory_frame)

class ViewCharacterInventoryFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.view_character_inventory_card = make_card(self)
        self.view_character_inventory_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.view_character_inventory_card,
            "Character Inventory"
        ).pack(padx=55, pady=(22, 4))

        self.inventory_character_selection_entry = make_entry(
            self.view_character_inventory_card,
            placeholder_text = "Character's name"
        )
        self.inventory_character_selection_entry.pack(padx=55, pady=(10,8))

        make_primary_button(
            self.view_character_inventory_card,
            text = "View Inventory",
            command = self.on_view_character_inventory
        ).pack(padx=55, pady=(10,8))

        self.view_character_inventory_list = make_textbox(self.view_character_inventory_card, width=350, height=160)
        self.view_character_inventory_list.pack(padx=55, pady=(10,8))

        make_secondary_button(
            self.view_character_inventory_card,
            text = "Back to Inventory Management",
            command = self.go_to_inventory_management
        ).pack(padx=55, pady=(10,15))

        self.view_character_inventory_status_label = make_status_label(self.view_character_inventory_card)
        self.view_character_inventory_status_label.pack(padx=55, pady=(10,8))

        self.view_character_inventory_list.tag_config("label", foreground=ACCENT_BRIGHT)
        self.view_character_inventory_list.tag_config("value", foreground=TEXT)
        self.view_character_inventory_list.tag_config("muted", foreground=TEXT_MUTED)

    def on_view_character_inventory(self):
        self.view_character_inventory_list.delete("1.0", "end")
        selected_character_name = self.inventory_character_selection_entry.get().strip()
        if not selected_character_name:
            self.view_character_inventory_status_label.configure(
                text="Please enter a character name",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

        inventory, error_message = get_inventory(self.app.cursor, selected_character_name)
        if error_message == "character not found":
            self.view_character_inventory_list.insert(
                "end",
                f"Character: {selected_character_name} not found",
                "muted",
            )
            return

        elif error_message == "no items in inventory":
            self.view_character_inventory_list.insert(
                "end",
                f"No items in {selected_character_name}'s inventory",
                "muted",
            )
            return

        else:
            for item in inventory:
                    self.view_character_inventory_list.insert("end", "Item: ", "label")
                    self.view_character_inventory_list.insert("end", f"{item[0]} ", "value")
                    self.view_character_inventory_list.insert("end", " | Quantity: ", "label")
                    self.view_character_inventory_list.insert("end", f"{item[1]}\n", "value")
            return

    def clear_status(self):
        self.view_character_inventory_status_label.configure(text="")

    def go_to_inventory_management(self):
        self.app.show_frame(self.app.inventory_frame)


class ViewItemQuantityFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.view_item_quantity_card = make_card(self)
        self.view_item_quantity_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.view_item_quantity_card,
            "Item Quantity"
        ).pack(padx=55, pady=(22, 4))

        self.inventory_character_selection_entry = make_entry(
            self.view_item_quantity_card,
            placeholder_text = "Character's name"
        )
        self.inventory_character_selection_entry.pack(padx=55, pady=(10,8))

        self.inventory_item_selection_entry = make_entry(
            self.view_item_quantity_card,
            placeholder_text = "Item's name"
        )
        self.inventory_item_selection_entry.pack(padx=55, pady=(10,8))


        make_primary_button(
            self.view_item_quantity_card,
            text = "View Quantity",
            command = self.on_view_item_quantity
        ).pack(padx=55, pady=(10,8))

        make_secondary_button(
            self.view_item_quantity_card,
            text = "Back to Inventory Management",
            command = self.go_to_inventory_management
        ).pack(padx=55, pady=(10,15))

        self.view_item_quantity_status_label = make_status_label(self.view_item_quantity_card)
        self.view_item_quantity_status_label.pack(padx=55, pady=(10,8))

    def on_view_item_quantity(self):
        selected_character_name = self.inventory_character_selection_entry.get().strip()
        selected_item_name = self.inventory_item_selection_entry.get().strip()

        if not selected_character_name or not selected_item_name:
            self.view_item_quantity_status_label.configure(
                text="Please enter a character name and item name",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            return

    
        quantity, error_message = get_item_quantity(self.app.cursor, selected_character_name, selected_item_name)
        if error_message == "character not found":
            self.view_item_quantity_status_label.configure(
                text = f"Character: {selected_character_name} not found",
                text_color=ERROR
            )
            self.after(3000, self.clear_status)
            return
        elif error_message == "item not found":
            self.view_item_quantity_status_label.configure(
                text = f"Item: {selected_item_name} not found",
                text_color=ERROR
            )
            self.after(3000, self.clear_status)
            return

        elif error_message == "not_in_inventory":
            self.view_item_quantity_status_label.configure(
                text = f"No such item in {selected_character_name}'s inventory",
                text_color=ERROR
            )
            self.after(3000, self.clear_status)
            return

        else:
            if quantity > 1:
                self.view_item_quantity_status_label.configure(
                    text = f"{selected_character_name} has {quantity} {selected_item_name}'s in their inventory",
                    text_color=SUCCESS
                    )
                self.after(3000, self.clear_status)
                return
                
            elif quantity == 1:
                self.view_item_quantity_status_label.configure(
                    text = f"{selected_character_name} has {quantity} {selected_item_name} in their inventory",
                    text_color=SUCCESS
                )
                self.after(3000, self.clear_status)
                return

    def clear_status(self):
        self.view_item_quantity_status_label.configure(text="")

    def go_to_inventory_management(self):
        self.app.show_frame(self.app.inventory_frame)

