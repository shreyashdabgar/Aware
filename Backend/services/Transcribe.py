import os 
import subprocess
from flask import Blueprint,render_template,redirect,request,session,jsonify
from faster_whisper import WhisperModel


Transcribe_bp = Blueprint('transcribe', __name__)
#object for whispermodel 
model = WhisperModel("small")

def SpeechToText(audio_path):
    try:
        segments , info = model.transcribe(audio_path)
        transcript = []
        
        for i in segments :
            print(i.start,i.end,i.text)

            transcript.append({
                'start': i.start,
                'end': i.end,
                'text':i.text
            })
        return transcript
    except Exception as e :
        print("there is some Error in SppechToText function",e)

def store_Transcript(transcript):
    try:
        pass
    except Exception as e :
        print("there is an Exception in storage oF TRANSCRIPTION")