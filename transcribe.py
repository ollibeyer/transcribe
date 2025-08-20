#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import timedelta
from typing import List

try:
	from faster_whisper import WhisperModel
	from tqdm import tqdm
except Exception as exc:
	print("Required packages not installed. Please run: pip install -r requirements.txt", file=sys.stderr)
	raise


def format_timestamp(seconds: float) -> str:
	milliseconds = int(seconds * 1000)
	return str(timedelta(milliseconds=milliseconds))


def transcribe_to_text(
	input_path: str,
	output_path: str,
	model_size: str = "large-v3",
	device: str = "auto",
	compute_type: str = "int8",
	language: str = "de",
	vad_filter: bool = True,
	print_timestamps: bool = False,
) -> None:
	if not os.path.exists(input_path):
		raise FileNotFoundError(f"Input audio not found: {input_path}")

	print(f"Loading model '{model_size}' (device={device}, compute_type={compute_type})...")
	model = WhisperModel(model_size, device=device, compute_type=compute_type)

	print("Transcribing... This may take a while depending on your CPU/GPU and model size.")
	
	# Get audio duration for progress estimation
	import subprocess
	try:
		result = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', input_path], 
							   capture_output=True, text=True, check=True)
		audio_duration = float(result.stdout.strip())
		print(f"Audio duration: {timedelta(seconds=int(audio_duration))}")
	except:
		audio_duration = None
		print("Could not determine audio duration for progress tracking")

	segments, info = model.transcribe(
		input_path,
		language=language,
		task="transcribe",
		vad_filter=vad_filter,
	)

	lines: List[str] = []
	segment_count = 0
	
	# Create progress bar
	with tqdm(desc="Transcribing", unit="segments") as pbar:
		for segment in segments:
			text = segment.text.strip()
			if not text:
				continue
				
			segment_count += 1
			
			# Update progress bar with current segment info
			if audio_duration:
				progress = (segment.end / audio_duration) * 100
				pbar.set_postfix({
					'Progress': f"{progress:.1f}%",
					'Current': f"{format_timestamp(segment.start)}-{format_timestamp(segment.end)}",
					'Segments': segment_count
				})
			else:
				pbar.set_postfix({
					'Current': f"{format_timestamp(segment.start)}-{format_timestamp(segment.end)}",
					'Segments': segment_count
				})
			
			if print_timestamps:
				start = format_timestamp(segment.start)
				end = format_timestamp(segment.end)
				lines.append(f"[{start} -> {end}] {text}")
			else:
				lines.append(text)
			
			pbar.update(1)

	# Join with newlines to keep sentence/segment boundaries clear
	output_text = "\n".join(lines).strip() + "\n"

	with open(output_path, "w", encoding="utf-8") as f:
		f.write(output_text)

	print(f"Done. Wrote transcript to: {output_path}")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Transcribe an audio file to German text using faster-whisper.")
	parser.add_argument(
		"--input",
		dest="input_path",
		default="Interview_KR.mp3",
		help="Path to input audio file (default: Interview_KR.mp3)",
	)
	parser.add_argument(
		"--output",
		dest="output_path",
		default="Interview_KR.txt",
		help="Path to output text file (default: Interview_KR.txt)",
	)
	parser.add_argument(
		"--model-size",
		dest="model_size",
		default="large-v3",
		choices=[
			"tiny", "base", "small", "medium", "large-v2", "large-v3",
		],
		help="Whisper model size (default: large-v3)",
	)
	parser.add_argument(
		"--device",
		dest="device",
		default="auto",
		choices=["auto", "cpu", "cuda"],
		help="Device to run on (default: auto)",
	)
	parser.add_argument(
		"--compute-type",
		dest="compute_type",
		default="int8",
		choices=["int8", "int8_float16", "float16", "float32"],
		help="Precision (default: int8 for faster CPU inference)",
	)
	parser.add_argument(
		"--no-vad",
		action="store_true",
		help="Disable VAD filter (voice activity detection)",
	)
	parser.add_argument(
		"--timestamps",
		action="store_true",
		help="Include timestamps for each segment in the output",
	)
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	try:
		transcribe_to_text(
			input_path=args.input_path,
			output_path=args.output_path,
			model_size=args.model_size,
			device=args.device,
			compute_type=args.compute_type,
			language="de",
			vad_filter=not args.no_vad,
			print_timestamps=args.timestamps,
		)
	except Exception as exc:
		print(f"Error: {exc}", file=sys.stderr)
		sys.exit(1)
