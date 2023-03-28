#!/usr/bin/env python3
# Author: Thoxvi <Dev@Thoxvi.com>


import click
from rich.console import Console

from ata import AudioRecorder

console = Console()


@click.command()
@click.option('--output', default="audio.mp3", help='音频文件保存位置')
@click.option('--sample-rate', default=44100, help='采样率')
@click.option('--channels', default=1, help='声道数（1 为单声道，2 为立体声）')
@click.option('--duration', default=10, help='最大录制时间（秒）')
@click.option('--threshold', default=0.1, help='音量阈值')
@click.option('--window-duration', default=1, help='时间窗口长度（秒）')
@click.option('--print-interval', default=0.5, help='音量平均值打印间隔（秒）')
def main(output, sample_rate, channels, duration, threshold, window_duration, print_interval):
    recorder = AudioRecorder(
        sample_rate=sample_rate,
        channels=channels,
        duration=duration,
        threshold=threshold,
        window_duration=window_duration,
        print_interval=print_interval,
    )
    recorder.record()
    recorder.save(output)
    console.print(f"录音已保存至 {output}", style="bold green")


if __name__ == "__main__":
    main()
