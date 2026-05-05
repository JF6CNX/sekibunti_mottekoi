@echo off
setlocal
cd /d %~dp0

:: 文字化け防止（UTF-8設定）
chcp 65001 >nul

echo ==========================================
echo    NMR集計ツール セットアップ ＆ 起動
echo ==========================================

:: Pythonが入っているか確認
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pythonがインストールされていません。
    pause
    exit /b
)

:: 仮想環境の作成
if not exist ".venv" (
    echo [1/3] 実行環境を作成中...
    python -m venv .venv
)

:: 仮想環境を使ってライブラリをインストール
echo [2/3] ライブラリをインストール中...
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install flet openpyxl

:: アプリ起動
echo [3/3] アプリを起動しています...
python app.py

if %errorlevel% neq 0 (
    echo.
    echo アプリの起動に失敗しました。
    pause
)