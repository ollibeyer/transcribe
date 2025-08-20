Local German Transcription with faster-whisper

Prerequisites (Windows):
- Python 3.9–3.12 installed and on PATH
- FFmpeg installed and on PATH (required for audio decoding)
  - Option A (winget): `winget install Gyan.FFmpeg`
  - Option B (Chocolatey): `choco install ffmpeg -y`
  - Option C: Download a static build from the FFmpeg website and add its `bin` folder to PATH

Setup
1) Open PowerShell in this folder:
```
cd "C:\Users\BeyerOl\workspace\transcribe"
```
2) Create and activate a virtual environment:
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
3) Install dependencies:
```
pip install --upgrade pip
pip install -r requirements.txt
```

Usage
- Place your audio file (e.g., `Interview_KR.mp3`) in this folder.
- Run the transcription (German, local, no cloud):
```
python transcribe.py --input Interview_KR.mp3 --output Interview_KR.txt --model-size large-v3 --compute-type int8
```

Notes
- The first run will download the selected model. `large-v3` is most accurate but slower; you can try `medium` for a faster baseline.
- If you have an NVIDIA GPU and CUDA installed, set `--device cuda` and consider `--compute-type float16`.
- Add `--timestamps` to include per-segment timestamps in the output file.
- If FFmpeg is not found, ensure its `bin` directory is on your PATH and restart your shell.
