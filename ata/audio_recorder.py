#!/usr/bin/env python3
# Author: Thoxvi <Dev@Thoxvi.com>

from rich.progress import Progress, BarColumn
from rich.console import Console
from pydub import AudioSegment
import sounddevice as sd
import numpy as np
from collections import deque
import time
import io

__all__ = [
    "AudioRecorder",
]


class AudioRecorder:
    def __init__(
        self,
        sample_rate=44100,
        channels=1,
        duration=10,
        threshold=0.3,
        window_duration=1,
        print_interval=0.5
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration
        self.threshold = threshold
        self.window_duration = window_duration
        self.print_interval = print_interval

        self.buffer = None
        self.recording = False
        self.stop_recording = False
        self.start_time = None
        self.volume_window = deque()
        self.last_print_time = 0

    def _callback(self, indata, frames, time_info, status):
        volume_norm = np.linalg.norm(indata) * 10
        self.volume_window.append(volume_norm)
        if len(self.volume_window) > self.sample_rate * self.window_duration // frames:
            self.volume_window.popleft()

        average_volume = np.mean(self.volume_window)
        current_time = time.time()
        if current_time - self.last_print_time > self.print_interval:
            self.progress.update(
                self.task, completed=int(average_volume * 100))
            self.last_print_time = current_time

        if not self.recording and average_volume > self.threshold:
            self.console.print("开始录制")
            self.recording = True
            self.start_time = current_time

        if self.recording and average_volume < self.threshold:
            self.console.print("结束录制")
            self.stop_recording = True

        if self.recording:
            self.buffer.write(
                (indata * np.iinfo(np.int16).max).astype(np.int16).tobytes())

            if current_time - self.start_time > self.duration:
                self.console.print("录制超时")
                self.stop_recording = True

        if self.stop_recording:
            raise sd.CallbackStop

    def record(self) -> None:
        self.buffer = io.BytesIO()
        self.recording = False
        self.stop_recording = False
        self.start_time = None
        self.last_print_time = time.time()

        self.console = Console()
        self.progress = Progress(BarColumn(), "[bold cyan]{task.description}")
        self.task = self.progress.add_task("[cyan]音量平均值", total=100)

        with self.progress:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self._callback
            ):
                while not self.stop_recording:
                    sd.sleep(100)

    def save(self, file_name) -> None:
        audio_data = self.buffer.getvalue()
        audio_segment = AudioSegment.from_mono_audiosegments(
            AudioSegment.from_file(
                io.BytesIO(audio_data),
                format="raw",
                frame_rate=self.sample_rate,
                channels=self.channels,
                sample_width=2)
        )
        audio_segment.export(
            file_name,
            format="mp3"
        )
        self.console.print("保存完成")
