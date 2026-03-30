@echo off
echo Setting up AudioBook Generator...
echo.

REM Set OpenRouter API key
set OPENROUTER_API_KEY=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

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To run the application:
echo   streamlit run app.py
echo.
pause
