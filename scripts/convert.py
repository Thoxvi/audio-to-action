#!/usr/bin/env python3
# Author: Thoxvi <Dev@Thoxvi.com>

import sys
import os
import click
from rich.console import Console

from ata import OpenAIAdapter

console = Console()


@click.command()
@click.argument("audio_file_path", type=click.Path(exists=True))
@click.option("--api_key", help="OpenAI API Key", default=os.environ.get("OPENAI_API_KEY"))
@click.option("--api_base", default=os.environ.get("OPENAI_API_BASE"), help="API Base URL")
@click.option("--language", default="zh", help="Language of the audio file, need to in the ISO 639-1 format")
@click.option("--map_file", default="data/map.json", help="Map file path")
@click.option("--prompts_file", default="data/prompts.txt", help="Prompts file path")
def conversion(api_key, api_base, audio_file_path, language, map_file, prompts_file):
    adapter = OpenAIAdapter(api_key, api_base)
    text = adapter.audio2text(audio_file_path, language)
    if text is None:
        console.print("Transcription failed", style="bold red")
        sys.exit(1)

    console.print(f"Transcribed text: {text}", style="bold green")

    value = adapter.text2value(
        text,
        prompts_file,
        map_file,
    )
    if not value:
        sys.exit(1)

    console.print(f"Value: {value}", style="bold green")


if __name__ == "__main__":
    conversion()
