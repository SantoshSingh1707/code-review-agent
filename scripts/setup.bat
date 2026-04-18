@echo off
echo Setting up Code Review Agent...

echo Installing Python dependencies...
pip install -r requirements.txt

echo Pulling CodeLlama model...
ollama pull codellama

if not exist .env copy .env.example .env

echo Setup complete!
echo Run 'python run.py' to start the API
pause
