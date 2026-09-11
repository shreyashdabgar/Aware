from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from Backend.models.user import User

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
        return jsonify({'error': str(e)}), 500