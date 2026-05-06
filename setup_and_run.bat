@echo off
chcp 65001 > nul

cd /d %~dp0

echo ==========================================
echo   NMRツール セットアップ ＆ 起動
echo ==========================================

where python > nul 2>&1
if %errorlevel% neq 0 (
    echo Pythonが見つかりません
    pause
    exit /b
)

if not exist venv (
    echo [1/3] 仮想環境を作成中...
    python -m venv venv
)

call venv\Scripts\activate

echo [2/3] ライブラリをインストール中...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [3/3] アプリ起動中...
python app.py

pause