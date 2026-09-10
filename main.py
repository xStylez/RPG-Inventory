import customtkinter as ctk 
from characters_screen import CharactersFrame, CreateCharacterFrame, ListCharactersFrame, SearchCharacterFrame, LevelUpCharacterFrame
from items_screen import ItemsFrame, CreateItemFrame, ListItemsFrame, SearchItemFrame, UpdateItemFrame, DeleteItemFrame, RemoveItemFromInventoriesFrame
from db import get_connection, setup_database
from inventory_screen import InventoryFrame, AddItemToInventoryFrame, RemoveItemFromInventoryFrame, ViewCharacterInventoryFrame, ViewItemQuantityFrame
from theme import BG_APP, BG_CARD, BG_INPUT, ACCENT, ACCENT_HOVER, TEXT, TEXT_MUTED, SUCCESS, ERROR, BORDER, make_card, make_title, make_subtitle, make_entry, make_primary_button, make_secondary_button, make_status_label
# set the appearance mode
ctk.set_appearance_mode("dark")

# set the default color theme
ctk.set_default_color_theme("dark-blue")

# main application class
class App (ctk.CTk):
    def __init__(self): # constructor
        super().__init__() # initialize the parent class
        setup_database()
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")

        # set the title and geometry of the window
        self.title("RPG Inventory Manager")
        self.geometry("1200x800")

        self.configure(fg_color=BG_APP)
        self.welcome_frame = ctk.CTkFrame(self, fg_color=BG_APP)
        self.welcome_frame.pack(fill="both", expand=True)

        self.welcome_card = make_card(self.welcome_frame)
        self.welcome_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(self.welcome_card, "Login").pack(padx=40, pady=(36, 6))
        make_subtitle(self.welcome_card, "Sign in to manage your RPG inventory").pack(padx=40, pady=(0, 20))

        self.username_entry = make_entry(self.welcome_card, placeholder_text="Username")
        self.username_entry.pack(padx=40, pady=8)

        self.password_entry = make_entry(self.welcome_card, placeholder_text="Password", show="*")
        self.password_entry.pack(padx=40, pady=8)

        make_primary_button(self.welcome_card, "Login", command=self.on_login_button_clicked).pack(padx=40, pady=(20, 8))

        self.login_status_label = make_status_label(self.welcome_card)
        self.login_status_label.pack(padx= 40,pady=(10,10))

        # create the menu frame
        self.menu_frame = ctk.CTkFrame(self, fg_color=BG_APP)
        self.menu_card = make_card(self.menu_frame)
        self.menu_card.place(relx=0.5, rely=0.5, anchor="center")
        make_title(self.menu_card, "Menu").pack(padx=40, pady=(22, 4))
        make_subtitle(self.menu_card, "Select an option from the menu").pack(padx=40, pady=(0, 10))

        # create the buttons for the menu
        make_primary_button(self.menu_card, "Characters", command = self.on_characters_button_clicked).pack(padx=55, pady=(10,8))
        make_primary_button(self.menu_card, "Items", command = self.on_items_button_clicked).pack(padx=55, pady=(20,8))
        make_primary_button(self.menu_card, "Inventory", command = self.on_inventory_button_clicked).pack(padx=55, pady=(20,8))
        make_secondary_button(self.menu_card, "Logout", command = self.on_logout_button_clicked).pack(padx=55, pady=(20,30))

        # Connections to character's frames from other files
        self.characters_frame = CharactersFrame(self, app=self)
        self.create_character_frame = CreateCharacterFrame(self, app=self)
        self.list_characters_frame = ListCharactersFrame(self, app=self)
        self.search_character_frame = SearchCharacterFrame(self, app=self)
        self.level_up_character_frame = LevelUpCharacterFrame(self, app=self)

        # Connections to items frames from other files
        self.items_frame = ItemsFrame(self, app=self)
        self.create_item_frame = CreateItemFrame(self, app=self)
        self.list_items_frame = ListItemsFrame(self, app=self)
        self.search_item_frame = SearchItemFrame(self, app=self)
        self.remove_item_from_inventories_frame = RemoveItemFromInventoriesFrame(self, app=self)
        self.update_item_frame = UpdateItemFrame(self, app=self)
        self.delete_item_frame = DeleteItemFrame(self, app=self)

        # Connections to inventory frames from other files
        self.inventory_frame = InventoryFrame(self, app=self) # create the inventory frame
        self.add_item_to_inventory_frame = AddItemToInventoryFrame(self, app=self)
        self.remove_item_from_inventory_frame = RemoveItemFromInventoryFrame(self, app=self)
        self.view_character_inventory_frame = ViewCharacterInventoryFrame(self, app=self)
        self.view_item_quantity_frame = ViewItemQuantityFrame(self, app=self)


    # on logout button clicked
    def on_logout_button_clicked(self):
        self.login_status_label.configure(text="")
        self.show_frame(self.welcome_frame)

    # on start button clicked
    def on_login_button_clicked(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "" or password == "":
            self.login_status_label.configure(
                text="Please fill in all fields",
                text_color= "orange"
                )
            self.after(3000, lambda:self.login_status_label.configure(text=""))
            return

        if username == "admin" and password == "admin123":
            self.login_status_label.configure(
                text="Login successful",
                text_color=SUCCESS
                )
            self.after(2000, lambda:self.login_status_label.configure(text=""))
            self.after(1500, lambda:self.show_frame(self.menu_frame))
        else:
            self.login_status_label.configure(
                text="Invalid username or password",
                text_color=ERROR
                )
            self.after(3000, lambda:self.login_status_label.configure(text=""))

    def on_characters_button_clicked(self):
        self.show_frame(self.characters_frame)

    def on_items_button_clicked(self):
        self.show_frame(self.items_frame)

    def on_inventory_button_clicked(self):
        self.show_frame(self.inventory_frame)

    
    # show the frame
    def show_frame(self, frame_to_show):
        for frame in (
            self.welcome_frame,
            self.menu_frame,
            self.characters_frame,
            self.items_frame,
            self.inventory_frame,
            self.create_character_frame,
            self.list_characters_frame,
            self.search_character_frame,
            self.level_up_character_frame,
            self.create_item_frame,
            self.list_items_frame,
            self.search_item_frame,
            self.update_item_frame,
            self.remove_item_from_inventories_frame,
            self.delete_item_frame,
            self.inventory_frame,
            self.add_item_to_inventory_frame,
            self.remove_item_from_inventory_frame,
            self.view_character_inventory_frame,
            self.view_item_quantity_frame,
        ):
            frame.pack_forget() # hide the frame
        frame_to_show.pack(fill ="both", expand = True) # show the frame
    

    # go to menu
    def go_to_menu(self):
        self.show_frame(self.menu_frame)    
    

# main function
if __name__ == "__main__":
    app = App() # create the application instance
    app.mainloop() # start the main event loop




