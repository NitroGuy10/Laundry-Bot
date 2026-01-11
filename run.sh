#!/bin/bash
SCRIPT_DIR=$(cd $(dirname "$0") && pwd)
cd $SCRIPT_DIR

# Wait for connection to be good
until ping -c1 discord.com; do sleep 5; done

source venv/bin/activate
python main.py 
