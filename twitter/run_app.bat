@echo off
echo Starting Twitter Sentiment Analysis Dashboard...
echo.
echo If you get an error about streamlit not being found, try:
echo 1. Install requirements: pip install -r requirements.txt
echo 2. Run with: python -m streamlit run app.py
echo.
python -m streamlit run app.py
pause