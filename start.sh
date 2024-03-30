#!/bin/bash

cd /root/home/Lottery
source venv/bin/activate
screen -dmS lottery_app sudo python3 app/main.py

cd /root/home/Lottery
source venv/bin/activate
screen -dmS lottery_app sudo python3 BOT/bot.py