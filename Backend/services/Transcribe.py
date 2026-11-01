import os 
import subprocess
from flask import Blueprint, render_template, redirect, request, session, jsonify
from faster_whisper import WhisperModel
import time

Transcribe_bp = Blueprint('transcribe', __name__)

start = time.perf_counter()


model = WhisperModel(
    "large-v3-turbo",                    # Uses your existing local file (No download needed)
    device="cuda",
    compute_type="int8_float16"  # Compresses the memory footprint to fit your 4GB VRAM
)

load_time = time.perf_counter() - start
print(f"Model loading time: {load_time:.2f} seconds")


def SpeechToText(audio_path, language_code=None):
    try:
        start = time.perf_counter()

        # Maximum speed settings
        segments, info = model.transcribe(
            audio_path,
            beam_size=1,            # 1 path decoding (Fastest)
            vad_filter=True,        # Skips silences
            language=language_code, # Optional language override
            condition_on_previous_text=False
        )
        
        transcript = []
        
        # No slow terminal prints inside the loop
        for i in segments:
            transcript.append({
                'start': i.start,
                'end': i.end,
                'text': i.text
            })

        transcription_time = time.perf_counter() - start
        audio_duration = info.duration

        print("\n========== OPTIMIZED BENCHMARK RESULTS ==========")
        print(f"Detected Language:    {info.language} ({info.language_probability:.2f})")
        print(f"Audio duration:       {audio_duration:.2f} seconds")
        print(f"Transcription time:   {transcription_time:.2f} seconds")
        if audio_duration > 0 and transcription_time > 0:
            print(f"Transcription speed:  {audio_duration / transcription_time:.2f}x real-time")
        print("=================================================\n")

        return transcript
    except Exception as e:
        print("There is some Error in SpeechToText function:", e)
