# In this file we can extract audio from a video
import os
import subprocess  # for ffmpeg

from flask import Blueprint, jsonify, session, render_template

from Backend.extensions import db
from Backend.services.chunk import chunks,Embeddings
from Backend.models.Transcript import Transcript
from Backend.models.videos import Video
from Backend.services.Transcribe import SpeechToText
from Backend.services.Chroma import store_chunks,serching_chunks,ask_question
from Backend.services.LLM import semantic_normalization
from sqlalchemy import inspect

preprocessing_bp = Blueprint('preprocessing', __name__)  # name of the blueprint is preprocessing


@preprocessing_bp.route('/processing/<int:video_id>')
def preprocessing(video_id):
    try:
        path = r'D:\Aware\uploads'
        video = Video.query.get_or_404(video_id)
        user_id = session.get('user_id')

        absolute_path = os.path.join(path, video.file_name)

        if video.user_id != user_id:
            return jsonify({'error': 'You are not allowed to process this video'}), 403

        if not os.path.exists(absolute_path):
            return jsonify({'error': 'There is no video available'}), 404


        #pipeline for video processing 

        audio_path = extract_audio(absolute_path)
        print("DEBUG: Audio extraction returned:", audio_path)
        transcript = SpeechToText(audio_path)
        print("DEBUG 2 - Transcript segments:", len(transcript or []))
        normalized = semantic_normalization(transcript)
        print("DEBUG 3 - Normalized segments:", len(normalized or []))
        Chunks = chunks(normalized)
        print("DEBUG 4 - Chunks:", len(Chunks or []))
        embedding = Embeddings(Chunks)
        print("DEBUG 5 - Embeddings:", type(embedding))
        vectorDB = store_chunks(embedding,Chunks,video.id)
        print("DEBUG 6 - Vector DB:", type(vectorDB), vectorDB)
        if not vectorDB:
            return "pipline is broken"

        # saving the data in to database(audio to text data save)
        

        print("=== ACTIVE PREPROCESSING DATABASE ===")
        print("Database URL:", db.engine.url)
        print(
            "Transcript columns:",
            [
                column["name"]
                for column in inspect(db.engine).get_columns("transcript")
            ]
        )
        print("=====================================")

        
# Save transcript segments to the database
       # Example of how your database insert loop should look:
        for segment in normalized:
            new_row = Transcript(
                video_id=video_id,
                start_time=segment['start'],
                end_time=segment['end'],
                text=segment['text'],                  # Maps to raw transcription text
                raw_text=segment['text'],              # Safe fallback to prevent 'raw_text' KeyError
                semantic_text=segment['semantic_text'] # Clean translated English
            )
            db.session.add(new_row)
        db.session.commit()

        return jsonify({
            "message": "audio extraction succesfully",
            "normalized_transcript": normalized
        })
    except Exception as e:
        print('There is an error in preprocessing function:', e)
        return jsonify({'error': 'There is an error in preprocessing function', 'details': str(e)}), 400


def extract_audio(absolute_path):
    try:
        audio_file = r'D:\Aware\Backend\audio'
        os.makedirs(audio_file, exist_ok=True)
        real_name = os.path.basename(absolute_path)
        name, _ = os.path.splitext(real_name)
        new_extension = name + '.wav'
        output_path = os.path.join(audio_file, new_extension)

        ffmpeg_path = r"D:\ffmpeg\ffmpeg-2026-09-21-git-a9cbcc2bbb-full_build\bin\ffmpeg.exe"
        command = [
            ffmpeg_path,
            '-y',
            '-i', absolute_path,
            '-vn',
            '-ac', '1',
            '-ar', '16000',
            '-c:a', 'pcm_s16le',
            '-threads', '0',
            output_path
        ]
        print('RUNNING FFMPEG:', command)
        subprocess.run(command, check=True)
        print('FFMPEG FINISHED')
        return output_path

    except Exception as e:
        print('There is some error in extract_audio function:', e)
        return ('there is an error in extract audio', e), 400

