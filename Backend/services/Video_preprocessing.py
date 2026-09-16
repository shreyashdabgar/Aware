# In this file we can exterect audio from video 

from flask import blueprints,render_template, redirect, session, request , jsonify, send_from_directory
from Backend.routes.main import video_file
preprocess_bp = blueprints('preprocessing', __name__)# name of the blue print is preprocessing 

@preprocess_bp.route('/processing/<int:video_id>')
def preprocessing(video_id):
    try :
        video_file()

    except Exception as e :
        print("there is an error in preprocessing function", e)
        return jsonify('there is an error in preprocessing function', e),400