Local German Transcription with faster-whisper

Prerequisites (Linux)
- Python 3.9–3.12 installed (`python3 --version`)
- FFmpeg installed (required for audio decoding)
  - Ubuntu/Debian: `sudo apt update && sudo apt install -y ffmpeg`
  - Fedora: `sudo dnf install -y ffmpeg`
  - Arch: `sudo pacman -S ffmpeg`

Setup
1) Open a terminal in this folder:
```
cd "/home/beyero/workspace/transcribe"
```
2) Create and activate a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```
3) Install dependencies:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4) Optional: make the script executable (Linux convenience):
```
chmod +x transcribe.py
```

Usage
- Place your audio file (e.g., `Interview_KR.mp3`) in this folder.
- Run the transcription (German, local, no cloud):
```
python3 transcribe.py --input Interview_KR.mp3 --output Interview_KR.txt --model-size large-v3 --compute-type int8
```
- Or, if you did step 4:
```
./transcribe.py --input Interview_KR.mp3 --output Interview_KR.txt --model-size large-v3 --compute-type int8
```

Notes
- The first run will download the selected model. `large-v3` is most accurate but slower; try `medium` for a faster baseline.
- NVIDIA GPU (optional): set `--device cuda` and consider `--compute-type float16` for speedups. On WSL2/Linux, ensure NVIDIA drivers and CUDA runtime are installed and accessible inside the distro.
- Add `--timestamps` to include per-segment timestamps in the output file.
- If FFmpeg is not found, install it as above and ensure `ffmpeg`/`ffprobe` are on your PATH (check with `which ffmpeg`).
