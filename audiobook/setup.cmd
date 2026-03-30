@echo off
echo Setting up AudioBook Generator...
echo.

REM Set OpenRouter API key
set OPENROUTER_API_KEY=your_api_key_here

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To run the application:
echo   streamlit run app.py
echo.
pause
