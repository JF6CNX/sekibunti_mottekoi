@echo off

chcp 65001
set PYTHONUTF8=1

call C:\Users\%USERNAME%\anaconda3\Scripts\activate.bat

conda env list | findstr nmr_env >nul
if errorlevel 1 (
    conda env create -f environment.yml
)

conda run -n nmr_env python tenpure_sakusei\main.py

pause