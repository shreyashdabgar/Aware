from flask import Flask, jsonify, render_template, request, session, url_for, redirect
from Backend.extensions import db
from Backend.models.user import User   
from Backend.routes.auth import auth_bp
from Backend.routes.main import main_bp


app = Flask(__name__, template_folder="../templates")
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.config['SECRET_KEY'] = 'some-secret-value'#session key for security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db.init_app(app)

with app.app_context():
    db.create_all()  # Create the database tables if they don't exist


@app.route('/')# Home page route
def home():
    return render_template('home.html') 


if __name__ == '__main__':
    app.run(debug = True)