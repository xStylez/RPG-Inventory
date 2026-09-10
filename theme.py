import customtkinter as ctk

BG_APP = "#0F1218"
BG_CARD = "#1A1F2E"
BG_INPUT = "#12161F"
ACCENT = "#7B61FF"
ACCENT_HOVER = "#6A4FE0"
ACCENT_BRIGHT = "#9B87FF"  # slightly brighter — list/search label tags
TEXT = "#FFFFFF"
TEXT_MUTED = "#8B93A7"
SUCCESS = "#2ECC71"
ERROR = "#FF5C7A"
BORDER = "#2A3145"

def make_card(parent, **kwargs):
    options = {
        "fg_color": BG_CARD,
        "corner_radius": 20,
        "border_width": 1,
        "border_color": BORDER,
    }
    options.update(kwargs)
    return ctk.CTkFrame(parent, **options)

def make_title(parent, text, **kwargs):
    options = {
        "text": text,
        "text_color": TEXT,
        "font": ("Segoe UI", 28, "bold"),
        "text_color": TEXT,
    }
    options.update(kwargs)
    return ctk.CTkLabel(parent, **options)

def make_subtitle(parent, text, **kwargs):
    options = {
        "text": text,
        "font": ("Segoe UI", 14),
        "text_color": TEXT_MUTED,
    }
    options.update(kwargs)
    return ctk.CTkLabel(parent, **options)

def make_entry(parent, placeholder_text="", show=None, **kwargs):
    options = {
        "placeholder_text": placeholder_text,
        "width": 280,
        "height": 40,
        "corner_radius": 12,
        "fg_color": BG_INPUT,
        "border_color": BORDER,
        "border_width": 1,
        "text_color": TEXT,
        "placeholder_text_color": TEXT_MUTED,
        "font": ("Segoe UI", 13),
    }
    if show is not None:
        options["show"] = show
    options.update(kwargs)
    return ctk.CTkEntry(parent, **options)

def make_primary_button(parent, text, command=None, **kwargs):
    options = {
        "text": text,
        "command": command,
        "width": 280,
        "height": 44,
        "corner_radius": 24,
        "fg_color": ACCENT,
        "hover_color": ACCENT_HOVER,
        "text_color": TEXT,
        "font": ("Segoe UI", 14, "bold"),
    }
    options.update(kwargs)
    return ctk.CTkButton(parent, **options)

def make_secondary_button(parent, text, command=None, **kwargs):
    # outlined style for Logout / Back
    options = {
        "text": text,
        "command": command,
        "width": 280,
        "height": 44,
        "corner_radius": 24,
        "fg_color": "transparent",
        "hover_color": BORDER,
        "border_width": 1,
        "border_color": BORDER,
        "text_color": TEXT,
        "font": ("Segoe UI", 14, "bold"),
    }
    options.update(kwargs)
    return ctk.CTkButton(parent, **options)

def make_status_label(parent, wraplength=None, justify=None, **kwargs):
    options = {
        "text": "",
        "font": ("Segoe UI", 14),
        "text_color": TEXT_MUTED,
    }
    if wraplength is not None:
        options["wraplength"] = wraplength
    if justify is not None:
        options["justify"] = justify
    options.update(kwargs)
    return ctk.CTkLabel(parent, **options)

def make_textbox(parent, width=400, height=200, **kwargs):
    options = {
        "width": width,
        "height": height,
        "corner_radius": 12,
        "fg_color": BG_INPUT,
        "border_color": BORDER,
        "border_width": 1,
        "text_color": TEXT,
        "font": ("Segoe UI", 13),
        "activate_scrollbars": True,
    }
    options.update(kwargs)
    return ctk.CTkTextbox(parent, **options)

def make_option_menu(parent, values, command=None, **kwargs):
    options = {
        "values": values,
        "command": command,
        "width": 280,
        "height": 44,
        "corner_radius": 12,          # less pill, more like an entry
        "fg_color": BG_INPUT,         # main field
        "button_color": ACCENT,       # arrow section (was default blue)
        "button_hover_color": ACCENT_HOVER,
        "text_color": TEXT,
        "dropdown_fg_color": BG_CARD,       # open list background
        "dropdown_hover_color": ACCENT,     # row hover
        "dropdown_text_color": TEXT,
        "font": ("Segoe UI", 13),
        "dropdown_font": ("Segoe UI", 13),
    }
    options.update(kwargs)
    return ctk.CTkOptionMenu(parent, **options)