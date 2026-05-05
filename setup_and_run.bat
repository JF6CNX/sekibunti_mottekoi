@echo off
setlocal
cd /d %~dp0

echo ==========================================
echo    NMR集計ツール セットアップ ＆ 起動
echo ==========================================

:: 1. 仮想環境の作成（最初の一回だけ）
if not exist ".venv" (
    echo [1/3] 実行環境を作成中... (初回のみ時間がかかります)
    python -m venv .venv
)

:: 2. 仮想環境の有効化とライブラリ更新
echo [2/3] 必要なライブラリをインストール・確認中...
call .venv\Scripts\activate
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

:: 3. アプリ起動
echo [3/3] アプリを起動しています...
python app.py

if %errorlevel% neq 0 (
    echo.
    echo アプリの起動に失敗しました。
    pause
)