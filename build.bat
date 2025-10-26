@echo off
echo Building RequirementImprover.exe...

pyinstaller --name="RequirementImprover" ^
  --onefile ^
  --windowed ^
  --add-data="prompts;prompts" ^
  --add-data="config.py;." ^
  --hidden-import="streamlit" ^
  --hidden-import="anthropic" ^
  --hidden-import="pandas" ^
  --collect-all="streamlit" ^
  app.py

echo Build complete!
pause