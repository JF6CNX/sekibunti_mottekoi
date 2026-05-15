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
    "sakura": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#FFF7F8",
        "panel": "#FFFFFF",
        "panel2": "#FCE7EC",
        "text": "#33272A",
        "card": "#F7D1DC",
        "selected": "#D85C82",
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
    "delphinium_dark": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#121A29",
        "bg_gradient": [
            "#182033",
            "#141D2E",
            "#10192A",
        ],
        "panel": "#1A2437",
        "panel_gradient": [
            "#1D2940",
            "#172133",
        ],
        "panel2": "#24304A",
        "panel2_gradient": [
            "#293653",
            "#202B43",
        ],
        "text": "#F3F7FF",
        "card": "#334363",
        "selected": "#4B73D9",
    },
    "blue_dragon_light": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#EAF5FF",
        "bg_gradient": [
            "#F4FAFF",
            "#EAF5FF",
            "#D7E9F7",
        ],
        "panel": "#F0F7FE",
        "panel_gradient": [
            "#F9FCFF",
            "#E4F0FA",
        ],
        "panel2": "#CFE4F5",
        "panel2_gradient": [
            "#DBECF8",
            "#BED9EE",
        ],
        "text": "#071A2B",
        "card": "#B8D3EA",
        "selected": "#1267D8",
    },
    "blue_dragon_dark": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#071A2B",
        "bg_gradient": [
            "#0B2740",
            "#071A2B",
            "#06213A",
        ],
        "panel": "#0E2742",
        "panel_gradient": [
            "#133150",
            "#0A2339",
        ],
        "panel2": "#12406A",
        "panel2_gradient": [
            "#16507F",
            "#0E3458",
        ],
        "text": "#F6FBFF",
        "card": "#1C557E",
        "selected": "#24D8FF",
    },
    "clownfish_light": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#FFF1E5",
        "bg_gradient": [
            "#FFF9F4",
            "#FFF1E5",
            "#FFE3CF",
        ],
        "panel": "#FFF8F3",
        "panel_gradient": [
            "#FFFDFC",
            "#FFEEDF",
        ],
        "panel2": "#FFD8BC",
        "panel2_gradient": [
            "#FFE5D0",
            "#FFCFAE",
        ],
        "text": "#1E2328",
        "card": "#F0C9A8",
        "selected": "#F47C20",
    },
    "clownfish_dark": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#18252B",
        "bg_gradient": [
            "#23363E",
            "#18252B",
            "#10181C",
        ],
        "panel": "#22343B",
        "panel_gradient": [
            "#2A4048",
            "#1D2D34",
        ],
        "panel2": "#2F474B",
        "panel2_gradient": [
            "#385559",
            "#293E42",
        ],
        "text": "#F8FAFC",
        "card": "#4C5A56",
        "selected": "#FF8A2A",
    },
    "duckweed_light": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#EEF7E2",
        "bg_gradient": [
            "#F7FBEF",
            "#EEF7E2",
            "#DCEEC5",
        ],
        "panel": "#F5FAEC",
        "panel_gradient": [
            "#FBFDF6",
            "#EBF5DE",
        ],
        "panel2": "#D4E8B9",
        "panel2_gradient": [
            "#E1F0CB",
            "#C4DBA6",
        ],
        "text": "#19322C",
        "card": "#BDD591",
        "selected": "#79C43C",
    },
    "momiji_light": {
        "mode": ft.ThemeMode.LIGHT,
        "bg": "#F8EADF",
        "bg_gradient": [
            "#FCF3EB",
            "#F8EADF",
            "#F2D8C4",
        ],
        "panel": "#FBF1E7",
        "panel_gradient": [
            "#FDF7F0",
            "#F6E4D3",
        ],
        "panel2": "#EDC7A5",
        "panel2_gradient": [
            "#F3D7BB",
            "#E3B289",
        ],
        "text": "#231B16",
        "card": "#D9A47A",
        "selected": "#D92D20",
    },
    "momiji_dark": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#231B16",
        "bg_gradient": [
            "#34271F",
            "#231B16",
            "#3B271E",
        ],
        "panel": "#4A3226",
        "panel_gradient": [
            "#5A3D2D",
            "#3E2A21",
        ],
        "panel2": "#6B412A",
        "panel2_gradient": [
            "#7E4D2F",
            "#5B3827",
        ],
        "text": "#FBF6EF",
        "card": "#8C5130",
        "selected": "#EF5A24",
    },
    "duckweed_dark": {
        "mode": ft.ThemeMode.DARK,
        "bg": "#102B29",
        "bg_gradient": [
            "#163734",
            "#102B29",
            "#0B201E",
        ],
        "panel": "#183B35",
        "panel_gradient": [
            "#1D4740",
            "#13332E",
        ],
        "panel2": "#29533E",
        "panel2_gradient": [
            "#34684C",
            "#214736",
        ],
        "text": "#EEF6EA",
        "card": "#466348",
        "selected": "#9EDB49",
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
