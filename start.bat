@echo off
setlocal
cd /d %~dp0

:: ���������h�~�iUTF-8�ݒ�j
chcp 65001 >nul

echo ==========================================
echo    NMR�W�v�c�[�� �Z�b�g�A�b�v �� �N��
echo ==========================================

:: Python�������Ă��邩�m�F
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python���C���X�g�[������Ă��܂���B
    pause
    exit /b
)

:: ���z���̍쐬
if not exist ".venv" (
    echo [1/3] ���s�����쐬��...
    python -m venv .venv
)

:: ���z�����g���ă��C�u�������C���X�g�[��
echo [2/3] ���C�u�������C���X�g�[����...
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install flet openpyxl

:: �A�v���N��
echo [3/3] �A�v�����N�����Ă��܂�...
python app.py

if %errorlevel% neq 0 (
    echo.
    echo �A�v���̋N���Ɏ��s���܂����B
    pause
)