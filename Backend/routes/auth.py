# creating Blueprints for auth
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from Backend.extensions import db
from Backend.models.user import User


# creating a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)#name of the blueprint is 'auth'


# Register route
@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
   if request.method == 'POST':
       name = request.form['name']
       email = request.form['email']
       password = request.form['password']

       # Check if the email already exists in the database
       user = User.query.filter_by(email=email).first()
       if user :
           return jsonify({'message': 'Email already exists'}), 400

       user = User(name=name, email=email, password=password)
       db.session.add(user)
       db.session.commit()
       return jsonify({'message': 'User registered successfully'}), 201

   return render_template('Register.html')  

# login route 
@auth_bp.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':# cheked user submmited the form
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.password == password:
            #session store 
            session['user_id'] = existing_user.id  # Store the user's ID in the session
            return redirect(url_for('home'))  # Redirect to the home page on successful login
        
        else:
            return jsonify({'message': 'Invalid email or password'}), 401

    

    return render_template('login.html')  # Render the login form


@auth_bp.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None) # deleting user id from session
    return redirect(url_for('home'))  # Redirect to the home page after logout