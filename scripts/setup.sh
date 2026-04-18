#!/bin/bash

echo "Setting up Code Review Agent..."

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Pulling CodeLlama model..."
ollama pull codellama

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please update it with your settings."
fi

echo "Setup complete!"
echo "Run 'python run.py' to start the API"
