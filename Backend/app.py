from flask import Flask, jsonify, render_template, request, session, url_for, redirect
from Backend.extensions import db
from Backend.models.user import User,Video
from Backend.routes.auth import auth_bp
from Backend.routes.main import main_bp
from Backend.services.Video_preprocessing import preprocess_bp
from datetime import timedelta


app = Flask(__name__, template_folder="../templates",static_folder='static',static_url_path='/static')
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(preprocess_bp)
app.config['SECRET_KEY'] = 'some-secret-value'#session key for security
app.config["PERMENENT_SESSION_LIFETIME"] = timedelta(minutes=30)#seting the time of session 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db.init_app(app)

with app.app_context():
    db.create_all()  # Create the database tables if they don't exist


@app.route('/')# Home page route
def home():
    return render_template('home.html') 


if __name__ == '__main__':
    app.run(debug = True)