import flet as ft

def get_theme_mode(theme_mode):
    if theme_mode == "dark":
        return ft.ThemeMode.DARK
    
    return ft.ThemeMode.LIGHT

def get_colors(theme_mode):
    dark = theme_mode == "dark"

    return {
        "bg": "#121212" if dark else "#F5F5F5",
        "panel": "#1E1E1E" if dark else "#FFFFFF",
        "panel2": "#262626" if dark else "#FFFFFF",
        "text": "white" if dark else "black",
        "card": "#333333" if dark else "#EAEAEA",
        "selected": "#1976D2",
    }