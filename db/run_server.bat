@echo off
title FastAPI Server - Armstrim
set PYTHONPATH=%PYTHONPATH%;%cd%
python -m uvicorn main:app --reload
pause