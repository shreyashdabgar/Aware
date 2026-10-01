# In this file we can extract audio from a video
import os
import subprocess  # for ffmpeg

from flask import Blueprint, jsonify, session

from Backend.extensions import db
from Backend.services.chunk import chunks
from Backend.models.Transcript import Transcript
from Backend.models.videos import Video
from Backend.services.Transcribe import SpeechToText

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

        if video.transcripts:
            return jsonify(" This video is already given for processing"),200

        
        audio_path = extract_audio(absolute_path)
        transcript = SpeechToText(audio_path)
        Chunks = chunks(transcript)

        # saving the data in to database(audio to text data save)
        for segment in transcript:
            obj = Transcript(
                text=segment['text'],
                video_id=video.id,
                start_time=segment['start'],
                end_time=segment['end']
            )

            db.session.add(obj)

        db.session.commit()
        return jsonify({
            'message': 'Video processed successfully',
            'transcript': transcript
        }), 200

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
            '-i',
            absolute_path,
            '-vn',
            '-acodec',
            'pcm_s16le',
            output_path
        ]
        print('RUNNING FFMPEG:', command)
        subprocess.run(command, check=True)
        print('FFMPEG FINISHED')
        return output_path

    except Exception as e:
        print('There is some error in extract_audio function:', e)
        return ('there is an error in extract audio', e), 400

