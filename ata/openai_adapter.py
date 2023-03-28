#!/usr/bin/env python3
# Author: Thoxvi <Dev@Thoxvi.com>

import os
import sys

from typing import Optional

import openai

from rich.console import Console

__all__ = [
    "OpenAIAdapter",
]

console = Console()


class OpenAIAdapter:
    def __init__(self, api_key, api_base=None):
        if not api_key:
            console.print(
                "Please provide an API key",
                style="bold red",
            )
            sys.exit(1)

        openai.api_key = api_key
        if api_base:
            openai.api_base = api_base

    def audio2text(self, audio_file_path, language) -> Optional[str]:
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    "whisper-1",
                    audio_file,
                    language=language,
                )
            return transcript.text
        except OpenAIError as err:
            console.print(
                f"Error while transcribing audio: {err}",
                style="bold red",
            )
            return None

    def text2value(text) -> Optional[str]:
        with open("map.json", "r") as f:
            map = f.read()

        with open("prompts.txt", "r") as f:
            prompts = f.read().format(map=map)
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": prompts,
                    },
                    {
                        "role": "user",
                        "content": text,
                    }
                ],
                top_p=0.1,
            )
            msg = completion.choices[0].message
            return msg["content"].strip()
        except OpenAIError as err:
            console.print(
                f"Error while transcribing audio: {err}",
                style="bold red",
            )
            return None
