from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from Backend.models.user import User, Video
from Backend.extensions import db
import uuid
import os 
# for unique title for every video

main_bp = Blueprint('main', __name__)# name of the blueprint is 'main'


@main_bp.route('/dashboard')
def dashboard():
    try :
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))  # Redirect to login if user is not logged in

        user_id  = session['user_id']
        user = User.query.get(user_id) #Fetch the user from the database using the user_id
        videos = Video.query.filter_by(user_id = user_id).all()  

        # sending the video and user to html form page
        return render_template('dashboard.html', user = user, videos = videos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

@main_bp.route('/upload', methods=['POST', 'GET'])
def upload_video():
    try:
        if request.method == 'POST':
            video = request.files['video_file']
            title = request.form['title']

            #must select file name 
            if not video.file_name:
                return jsonify('You must select Video'),200

            #cannot enter empty title
            if not title.strip(" "):
                return jsonify('you must have to enter Title'), 400

            
            #gives unique id to pervent overqrite becuase of same name 
            random_id = uuid.uuid4()

            split = os.path.splitext(video.file_name)
            random_name_uuid = str(random_id) + split[1]

            #checking that our file is actual video or not 
            ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm'}
            extension = split[1].lower().lstrip('.')
            if extension not in ALLOWED_EXTENSIONS:
                #save the video file in location
                 return jsonify('upload in this formet:', ALLOWED_EXTENSIONS), 200
            else :
                video.save(f'uploads/{random_name_uuid}')

            #creating Database record
            video_obj = Video(title=title,
                               file_name=random_name_uuid, 
                               user_id=session['user_id'])
            
            db.session.add(video_obj)
            db.session.commit()
            return redirect(url_for('main.dashboard'))  # Redirect to dashboard after successful upload
        
        return render_template('upload.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


'''If There is data came from url then you don't need post and get'''

@main_bp.route('/video/<int:video_id>')
def video(video_id):
    try:
        user_id = session['user_id']
        video = Video.query.get_or_404(video_id)

        if video.user_id == user_id:
            return render_template('video_details.html', video=video)

        return jsonify("you don't have this video"), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/video-file/<int:video_id>')
def video_file(video_id):
    try:
        user_id = session['user_id']
        video = Video.query.get_or_404(video_id)
        if video.user_id == user_id :
            filename = video.file_name
            actual_video = send_from_directory(
            directory=os.path.abspath('uploads'),
            path=filename
            )
            return actual_video
        else :
            return jsonify('there is error in file'),403
    except Exception as e :
        print("VIDEO ERROR:", e)
        return jsonify({'error': str(e)}), 500

