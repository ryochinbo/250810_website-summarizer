@echo off

call .venv\Scripts\activate

pip install --upgrade pip

streamlit run main.py

pause