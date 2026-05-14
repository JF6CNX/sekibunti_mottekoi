# NMR Manager

NMR Manager is a Flet-based desktop application for reading NMR `integrals`
files, selecting peak/integral numbers in a GUI, and exporting the selected
orders to Excel.

## Features

- Scan NMR sample folders automatically
- Select integral numbers from the GUI
- Save and apply selection templates
- Export selected integral data to Excel
- Switch between dark and light themes
- Keep user settings in local JSON files

## Project Structure

```text
sekibunti_mottekoi/
  app.py
  nmr_manager/
    excel_service.py
    integrals.py
    messages.py
    paths.py
    scanner.py
    settings.py
    state.py
    templates.py
    theme.py
    ui/
      main_view.py
      sample_panel.py
      settings_dialog.py
      template_panel.py
  nmr_excelsekibunti/
    core/
      excel_writer.py
  nmr_core/
  requirements.txt
  setup_and_run.bat
```

## Installation

Create and activate a virtual environment, then install dependencies.

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

## Local Data

The app stores local settings and templates in the `data/` directory. These
files are ignored by Git because they may contain user-specific paths.

```text
data/settings.json
data/nmr_v12_final.json
output/
```

## Build

If you need an executable, build it with Flet or PyInstaller according to your
local environment.

```powershell
flet pack app.py --name "NMR Manager"
```

Generated files such as `dist/`, `build/`, `.exe`, and `.xlsx` are ignored by
Git.
