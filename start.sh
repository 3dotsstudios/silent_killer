#!/bin/bash

echo "💀 Starting Silent Killer Flask server..."
python3 sever.py &

echo "🤖 Launching Silent Killer Telegram bot..."
python3 bot.py