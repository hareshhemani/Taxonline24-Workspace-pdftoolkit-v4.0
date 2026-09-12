@echo off
title Taxonline24 Workspace Launcher
echo =========================================
echo Starting Taxonline24 Document Workspace...
echo =========================================
echo.
echo Please wait while the local server starts. Your browser will open automatically.
echo (Do not close this black window while using the app)
echo.

:: Run the Streamlit app
python -m streamlit run app.py

:: Keep the window open if there is an error
pause