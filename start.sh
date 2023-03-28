#!/usr/bin/env bash
# Author: Thoxvi <Dev@Thoxvi.com>

cd "$(dirname "$0")"
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Check OPENAI_API_KEY
if [ -z "$OPENAI_API_KEY" ]; then
    echo "OPENAI_API_KEY not found"
    exit 1
fi

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
audio_file=cache/audio.mp3
while true;
do
    rm -f $audio_file
    python3 scripts/record.py --output $audio_file
    python3 scripts/convert.py $audio_file
    echo Sleeping...
    sleep 5
done
