import customtkinter as ctk
from characters import create_character, list_characters, get_character, character_level_up
from theme import BG_APP, BG_CARD, BG_INPUT, ACCENT, ACCENT_BRIGHT, ACCENT_HOVER, TEXT, TEXT_MUTED, SUCCESS, ERROR, BORDER, make_card, make_title, make_subtitle, make_entry, make_primary_button, make_secondary_button, make_status_label, make_option_menu, make_textbox


CLASSES = {
    "Warrior": "A highly skilled fighter with a focus on physical combat.",
    "Mage": "A master of magic who can cast spells and use magical abilities.",
    "Steelheart": "A highly skilled defensive warrior who can block attacks and protect allies.",
    "Assassin": "A master of stealth and agility who can use their skills to outmaneuver their enemies.",
    "Druid": "A master of nature who can use their skills to heal and support allies.",
}


class CharactersFrame(ctk.CTkFrame,):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.character_menu_card = make_card(self)
        self.character_menu_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.character_menu_card,
            text="Characters"
            ).pack(padx=55, pady=(22, 4)) # create the characters label
        
        make_subtitle(
            self.character_menu_card,
            text="Select an option to manage"
            ).pack(padx=55, pady=(0, 10))

        make_primary_button(
            self.character_menu_card,
            text = "Create Character",
            command = self.on_create_character_button_clicked
            ).pack(padx=55, pady=(10,8))

        make_primary_button(
            self.character_menu_card,
            "List All Characters",
            command = self.on_list_characters_button_clicked
            ).pack(padx=55, pady=(20,8))

        make_primary_button(
            self.character_menu_card,
            text = "Find a Character",
            command = self.on_find_character_button_clicked
            ).pack(padx=55, pady=(20,8))

        make_primary_button(
            self.character_menu_card,
            text = "Level Up a Character",
            command = self.on_character_level_up_button_clicked
            ).pack(padx=55, pady=(20,8))

        make_secondary_button(
            self.character_menu_card,
            text = "Back to Menu",
            command = self.go_to_menu
            ).pack(padx=55, pady=(20,30))
    
    def on_create_character_button_clicked(self):
        self.app.show_frame(self.app.create_character_frame)

    def on_list_characters_button_clicked(self):
        self.app.list_characters_frame.refresh_list()
        self.app.show_frame(self.app.list_characters_frame)

    def on_find_character_button_clicked(self):
        self.app.show_frame(self.app.search_character_frame)

    def on_character_level_up_button_clicked(self):
        self.app.show_frame(self.app.level_up_character_frame)


    # go to menu
    def go_to_menu(self):
        self.app.go_to_menu()

class CreateCharacterFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.create_character_card = make_card(self)
        self.create_character_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.create_character_card,
            text="Character Creation"
            ).pack(padx=55, pady=(22, 4))
        
        make_subtitle(
            self.create_character_card,
            text="Please fill the form to create a new character"
            ).pack(padx=55, pady=(0, 10))

        #character name entry
        self.create_character_name_entry = make_entry(
            self.create_character_card,
            placeholder_text = "Enter the name of the character",
        )
        self.create_character_name_entry.pack(padx=55, pady=(10,8)) # pack/show the characters name entry

        # create the characters class menu
        self.create_character_class_menu = make_option_menu( 
            self.create_character_card,
            values = list(CLASSES.keys()),
            command = self.on_create_character_class_selected,
        )
        self.create_character_class_menu.set(list(CLASSES.keys())[0]) # set the default character class
        self.create_character_class_menu.pack(padx=55, pady=(10,8)) # pack/show the characters class menu

        self.class_desc_box = ctk.CTkFrame(
            self.create_character_card,
            fg_color="transparent",
            width=300,
            height=80,
        )
        self.class_desc_box.pack(padx=55, pady=(10,8))
        self.class_desc_box.pack_propagate(False)

        # create the characters class description label
        self.create_character_class_description_label = ctk.CTkLabel(
            self.class_desc_box,
            text = CLASSES[list(CLASSES.keys())[0]],
            text_color=TEXT_MUTED,
            font = ("Segoe UI", 13),
            wraplength = 280,
            justify = "center",
        )
        self.create_character_class_description_label.pack(fill="both", expand=True, padx=10, pady=(10,8)) # pack/show the characters class description label)

        make_primary_button(
            self.create_character_card,
            text = "Create Character",
            command = self.on_create_character_button_clicked_create_character_frame,
        ).pack(padx=55, pady=(10,8))

        make_secondary_button(
            self.create_character_card,
            text= "Back to Characters menu",
            command = self.go_to_characters_frame
        ).pack(padx=55, pady=(20,20)) # create the back to characters button

        self.status_label = make_status_label(self.create_character_card)
        self.status_label.pack(padx=55, pady=(10,8))
    
        # update description label when character class is selected
    def on_create_character_class_selected(self, choice):
        self.create_character_class_description_label.configure(text = CLASSES[choice])

    def on_create_character_button_clicked_create_character_frame(self):
        name = self.create_character_name_entry.get().strip()
        class_name = self.create_character_class_menu.get()

        if not name:
            self.status_label.configure(
                text= "Please enter a character name",
                text_color="orange"
                )
            self.after(3000, self.clear_status)
            return
        
        created_character = create_character(self.app.cursor, name, class_name)
        
        if created_character:
            self.status_label.configure(
                text= f"Character {name} - {class_name} created successfully",
                text_color= SUCCESS
            )
            self.app.conn.commit()
            self.after(3000, self.clear_status)
            self.create_character_name_entry.delete(0, "end")
            return
        else:
            self.status_label.configure(
                text= f"Character {name} already exists",
                text_color= ERROR
            )
            self.after(3000, self.clear_status)
            return

    def clear_status(self):
        self.status_label.configure(text="")

    def go_to_characters_frame(self):
        self.app.show_frame(self.app.characters_frame) # called the show_frame method from the main app class, to go to the characters frame

    
class ListCharactersFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.list_characters_card = make_card(self)
        self.list_characters_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.list_characters_card,
            text="List of all characters"
            ).pack(padx=55, pady=(22, 4))

        self.list_characters_listbox = make_textbox(self.list_characters_card, height=250)
        self.list_characters_listbox.pack(pady=10, padx=20, fill="x") # pack/show the characters listbox
        self.list_characters_listbox.tag_config("label", foreground=ACCENT_BRIGHT)
        self.list_characters_listbox.tag_config("value", foreground=TEXT)
        self.list_characters_listbox.tag_config("muted", foreground=TEXT_MUTED)

        make_secondary_button(
            self.list_characters_card,
            text= "Back to Characters menu",
            command = self.go_to_characters_frame
        ).pack(padx=55, pady=(10,20))

    # refresh the list of characters ( init runs once at startup, so the list doesnt update after adding a character, needs refresh to update the list)
    def refresh_list(self):
        self.list_characters_listbox.delete("1.0", "end")
        
        characters = list_characters(self.app.cursor)
        if not characters:
            self.list_characters_listbox.insert("end", "No characters found", "muted")
        else:
            for character in characters:
                self.list_characters_listbox.insert("end", "ID: ", "label")
                self.list_characters_listbox.insert("end", f"{character[0]}  ", "value")
                self.list_characters_listbox.insert("end", "Name: ", "label")
                self.list_characters_listbox.insert("end", f"{character[1]}  ", "value")
                self.list_characters_listbox.insert("end", "Class: ", "label")
                self.list_characters_listbox.insert("end", f"{character[2]}  ", "value")
                self.list_characters_listbox.insert("end", "Level: ", "label")
                self.list_characters_listbox.insert("end", f"{character[3]}\n", "value")



    def go_to_characters_frame(self):
        self.app.show_frame(self.app.characters_frame) # called the show_frame method from the main app class, to go to the characters frame


class SearchCharacterFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.search_character_card = make_card(self)
        self.search_character_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.search_character_card,
            text="Character Information"
            ).pack(padx=55, pady=(22, 4))

        make_subtitle(
            self.search_character_card,
            text="Enter the name of the character to search"
            ).pack(padx=55, pady=(0, 10))

        self.search_character = make_entry(
            self.search_character_card,
            placeholder_text = "Enter the name of the character",
        )
        self.search_character.pack(padx=55, pady=(10,8)) # pack/show the search character entry

        make_primary_button(
            self.search_character_card,
            text= "Search Character",
            command = self.on_search_character_button_clicked
            ).pack(padx=55, pady=(10,8))

        self.search_character_listbox = make_textbox(self.search_character_card, height=150)
        self.search_character_listbox.pack(pady=10, padx=20, fill="x") # pack/show the characters listbox
        self.search_character_listbox.tag_config("label", foreground=ACCENT_BRIGHT)
        self.search_character_listbox.tag_config("value", foreground=TEXT)
        self.search_character_listbox.tag_config("muted", foreground=TEXT_MUTED)

        make_secondary_button(
            self.search_character_card,
            text= "Back to Characters menu",
            command = self.go_to_characters_frame
        ).pack(padx=55, pady=(10,10))

        self.search_character_status_label = make_status_label(self.search_character_card)
        self.search_character_status_label.pack(padx=55, pady=(10, 15))

    def go_to_characters_frame(self):
        self.app.show_frame(self.app.characters_frame) # called the show_frame method from the main app class, to go to the characters frame
    
    def on_search_character_button_clicked(self):
        character_name = self.search_character.get().strip()
        if not character_name:
            self.search_character_status_label.configure(
                text="Please enter a character name",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            self.search_character_listbox.delete(1.0, "end")
            print("Please enter a character name") #debugging
            return
        
        character_found = get_character(self.app.cursor, character_name)
        self.refresh_search_listbox(character_found, character_name)
        
    def refresh_search_listbox(self, character_found, character_name):
        self.search_character_listbox.delete("1.0", "end")

        if not character_found:
            self.search_character_listbox.insert(
                "end",
                f"Character {character_name} not found",
                "muted",
            )
            return

        self.search_character_listbox.insert("end", "ID: ", "label")
        self.search_character_listbox.insert("end", f"{character_found[0]}\n", "value")
        self.search_character_listbox.insert("end", "Name: ", "label")
        self.search_character_listbox.insert("end", f"{character_found[1]}\n", "value")
        self.search_character_listbox.insert("end", "Class: ", "label")
        self.search_character_listbox.insert("end", f"{character_found[2]}\n", "value")
        self.search_character_listbox.insert("end", "Level: ", "label")
        self.search_character_listbox.insert("end", f"{character_found[3]}\n", "value")

    def clear_status(self):
        self.search_character_status_label.configure(text="")

class LevelUpCharacterFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=BG_APP)
        self.app = app

        self.level_up_character_card = make_card(self)
        self.level_up_character_card.place(relx=0.5, rely=0.5, anchor="center")

        make_title(
            self.level_up_character_card,
            text="Level Up"
            ).pack(padx=55, pady=(22, 4))
  
        make_subtitle(
            self.level_up_character_card,
            text="Enter the name of the character to level up"
            ).pack(padx=55, pady=(0, 10))

        #character name entry
        self.level_up_character_name_entry = make_entry(
            self.level_up_character_card,
            placeholder_text = "Enter the name of the character",
        )
        self.level_up_character_name_entry.pack(padx=55, pady=(10,8)) # pack/show the characters name entry

        make_primary_button(
            self.level_up_character_card,
            text= "level up character",
            command = self.on_level_up_character_button_clicked
        ).pack(padx=55, pady=(10,8))

        make_secondary_button(
            self.level_up_character_card,
            text= "Back to Characters menu",
            command = self.go_to_characters_frame
        ).pack(padx=55, pady=(10,10))

        self.status_label = make_status_label(self.level_up_character_card)
        self.status_label.pack(padx=55, pady=(10,10))

    def go_to_characters_frame(self):
        self.app.show_frame(self.app.characters_frame) # called the show_frame method from the main app class, to go to the characters frame

    def on_level_up_character_button_clicked(self):
        character_name = self.level_up_character_name_entry.get().strip()
        if not character_name:
            self.status_label.configure(
                text="Please enter a character name",
                text_color="orange"
            )
            self.after(3000, self.clear_status)
            print("Please enter a character name") #debugging
            self.level_up_character_name_entry.delete(0, "end")
            return

        character_new_level = character_level_up(self.app.cursor, character_name)
        self.app.conn.commit()
        if not character_new_level:
            self.status_label.configure(
                text=f"Character {character_name} not found",
                text_color=ERROR 
                )
            self.after(3000, self.clear_status)
            self.level_up_character_name_entry.delete(0, "end")
            return
        else:
            self.status_label.configure(
                text= f"{character_name} has leveled up to level {character_new_level}",
                text_color=SUCCESS 
                )
            self.after(3000, self.clear_status)
            self.level_up_character_name_entry.delete(0, "end")
            return

    def clear_status(self):
        self.status_label.configure(text="")
