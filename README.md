# Audio To Action

## 这是什么？

这是一个支持录制音频到本地并通过 Whisper 转换到文字，再映射到 Action 的库。

库在 `./data/map.json` 目录下，可以自行修改。

## 依赖

> 没有为 Windows 测试（不过改改就能用）

安装 Python 依赖

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

安装 ffmpeg 用于录音

```bash
# MacOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg

# CentOS
sudo yum install ffmpeg

# 其他系统
# Download from https://ffmpeg.org/download.html
```

## 简单脚本使用方法

配置环境变量

- OPENAI_API_KEY
- OPENAI_API_BASE [可选] 例如 `https://api.openai.com/v1/`

```bash
bash ./start.sh
```
