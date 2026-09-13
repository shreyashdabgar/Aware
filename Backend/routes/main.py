from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from Backend.models.user import User, Video
from Backend.extensions import db

main_bp = Blueprint('main', __name__)# name of the blueprint is 'main'


@main_bp.route('/dashboard')
def dashboard():
    try :
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))  # Redirect to login if user is not logged in

        user_id  = session['user_id']
        user = User.query.get(user_id)  # Fetch the user from the database using the user_id

        return render_template('dashboard.html', user = user)
    except Exception as e:
        return jsonify({'error': str(e)}), 2000 

@main_bp.route('/upload', methods=['POST', 'GET'])
def upload_video():
    try:
        if request.method == 'POST':
            video = request.files['video_file']
            title = request.form['title']

            #save the video file in location
            video.save(f'uploads/{video.filename}')

            #creating Database record
            video_obj = Video(title=title,
                               file_name=video.filename, 
                               user_id=session['user_id'])
            
            db.session.add(video_obj)
            db.session.commit()
            return redirect(url_for('main.dashboard'))  # Redirect to dashboard after successful upload
            # Save the video file to a desired location (e.g., 'uploads' folder)
        return render_template('upload.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500