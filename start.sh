#!/bin/bash

source /root/home/Lottery/venv/bin/activate
screen -dmS lottery_app sudo python3 /root/home/Lottery/app/main.py

source /root/home/Lottery/venv/bin/activate
screen -dmS lottery_bot sudo python3 /root/home/Lottery/BOT/bot.py