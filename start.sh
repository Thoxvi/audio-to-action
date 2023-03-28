#!/usr/bin/env bash
# Author: Thoxvi <Dev@Thoxvi.com>

cd "$(dirname "$0")"
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Check ffmpeg
if ! which ffmpeg &> /dev/null; then
    echo "ffmpeg not found"
    exit 1
fi

# Check python3
if ! which python3 &> /dev/null; then
    echo "python3 not found"
    exit 1
fi

# Setup venv
if [ ! -d venv ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
clear

# Main
set -e
while true;
do
    python3 scripts/record.py --output cache/audio.mp3
    python3 scripts/convert.py cache/audio.mp3
    sleep 5
done
