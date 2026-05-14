import flet as ft


THEMES = {
    "dark": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#121212",
        "panel": "#1E1E1E",
        "panel2": "#262626",
        "text": "white",
        "card": "#333333",
        "selected": "#1976D2",
    },
    "light": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#F5F5F5",
        "panel": "#FFFFFF",
        "panel2": "#FFFFFF",
        "text": "black",
        "card": "#EAEAEA",
        "selected": "#1976D2",
    },
    "midnight": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#07111F",
        "panel": "#0E1B2E",
        "panel2": "#13243A",
        "text": "#F4F8FF",
        "card": "#20324F",
        "selected": "#4D8DFF",
    },
    "forest": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#101815",
        "panel": "#17221D",
        "panel2": "#1F2E27",
        "text": "#F2F7F3",
        "card": "#2A3A32",
        "selected": "#3BA776",
    },
    "laboratory": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#EEF5F7",
        "panel": "#FFFFFF",
        "panel2": "#E2EEF2",
        "text": "#1B2A30",
        "card": "#D5E5EA",
        "selected": "#168AAD",
    },
    "sakura": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#FFF7F8",
        "panel": "#FFFFFF",
        "panel2": "#FCE7EC",
        "text": "#33272A",
        "card": "#F7D1DC",
        "selected": "#D85C82",
    },
    "contrast": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#000000",
        "panel": "#111111",
        "panel2": "#1C1C1C",
        "text": "#FFFFFF",
        "card": "#2B2B2B",
        "selected": "#FFD400",
    },
    "discord": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#1E1F3A",
        "bg_gradient": [
            "#111827",
            "#25284F",
            "#5865F2",
        ],
        "panel": "#23243A",
        "panel_gradient": [
            "#23243A",
            "#2B2D55",
        ],
        "panel2": "#2B2D45",
        "panel2_gradient": [
            "#2B2D45",
            "#34365C",
        ],
        "text": "#F8F9FF",
        "card": "#363957",
        "selected": "#5865F2",
    },
    "abalone": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#F7F2EF",
        "bg_gradient": [
            "#FFF8F6",
            "#EAF8F5",
            "#D9F1EE",
            "#F6DDE7",
        ],
        "panel": "#FFFCFA",
        "panel_gradient": [
            "#FFFFFF",
            "#F5FBF9",
            "#FCEBF1",
        ],
        "panel2": "#F7ECEF",
        "panel2_gradient": [
            "#FFF7F9",
            "#E7F6F3",
            "#F8E2EA",
        ],
        "text": "#26383A",
        "card": "#E8F3F1",
        "selected": "#4FB7B4",
    },
}


def get_theme_names():
    return list(THEMES.keys())


def get_theme(theme_mode):
    return THEMES.get(theme_mode, THEMES["dark"])


def get_theme_mode(theme_mode):
    return get_theme(theme_mode)["mode"]


def get_colors(theme_mode):
    theme = get_theme(theme_mode)
    return {
        key: value
        for key, value in theme.items()
        if key != "mode"
    }
