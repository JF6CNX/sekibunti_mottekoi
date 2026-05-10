NMR Manager

NMR積分データ（integrals）を読み込み，GUI上でピーク番号を選択・並び替えし，Excelへ自動出力するためのFletベースのアプリケーションです．

Features
NMRサンプルの自動探索
積分番号（integral number）のGUI選択
選択順の保存
テンプレート保存 / 読み込み
複数サンプルへのテンプレ一括適用
Excel自動出力
Dark / Light テーマ切替
.exe 化対応
Supported Sample Names

以下のようなサンプル名に対応しています．

TTH-ABC-001
MKK-XYZ-002
FJK_TEST_003

先頭の研究者コードが異なっていても利用可能です．

Required Structure
project/
│
├─ app.py
├─ nmr_excelsekibunti/
│
├─ data/
│
├─ output/
│
└─ NMR sample folders
Installation
1. Create virtual environment
python -m venv venv
2. Activate virtual environment
Windows
.\venv\Scripts\activate
3. Install packages
pip install -r requirements.txt
Run Application
python app.py
Build EXE
flet pack app.py --name "NMR Manager"

Generated executable:

dist/app.exe
Settings

Application settings are stored in:

data/settings.json

Saved items:

Input directory
Output directory
Theme mode
Auto-open Excel option
Templates

Peak selection templates are stored in:

data/nmr_v12_final.json
Excel Export

Selected integral orders are exported using:

write_excel_from_integrals_multi()

from:

nmr_excelsekibunti.core.excel_writer
Main Libraries
Flet
OpenPyXL
JSON
Regular Expressions (re)
Recommended .gitignore
__pycache__/
*.pyc

venv/
build/
dist/

output/

data/settings.json

.vscode/
Notes
Avoid building inside OneDrive directories if possible.
EXE generation is more stable inside local directories such as:
C:\dev\
If EXE does not launch, install Microsoft Visual C++ Redistributable.
License

Private research / laboratory use.
