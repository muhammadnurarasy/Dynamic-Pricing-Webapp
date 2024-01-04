from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import LoginManager, login_required, current_user, logout_user, login_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_bcrypt import Bcrypt
import requests
from datetime import datetime
from wtforms import StringField, PasswordField, validators
import os
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly
import json

app = Flask(__name__)
logger = app.logger
FASTAPI_ENDPOINT = "http://fastapi-app:8000/predict"

def format_date(value, date_format='%Y'):
    return value.strftime(date_format)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app.jinja_env.filters['date'] = format_date
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)  # for example, remember the user for 14 days
app.config['SECRET_KEY'] = 'arasy'  # Change 'yoursecretkey' to a random string for security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    profile_image = db.Column(db.String(120), nullable=True, default='default.png')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # The function name of our future login route

bcrypt = Bcrypt(app)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8, max=128),
        validators.Regexp(
            r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])', 
            message="Password must have 1 uppercase, 1 lowercase, 1 number, and 1 special symbol"
        )
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Optional: Check if the email and username aren't already taken
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Please choose a different one.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')  
    submit = SubmitField('Login')

# Load your dataset here
data = pd.read_csv('adjusted_price_real_estate_data.csv')

def create_bar_chart():
    # Replace 'Property_Type' with the actual column name in your dataset
    counts = data['Property_Type'].value_counts()
    bar_chart = go.Figure(data=go.Bar(x=counts.index, y=counts.values))
    bar_chart.update_layout(title='Distribution of Property Types')
    return bar_chart.to_json()



@app.route('/')
def index():
    if current_user.is_authenticated:
        logger.info("Profile Image: %s", current_user.profile_image)
        return redirect(url_for('dashboard'))
    # If not authenticated, render the registration or login form
    return render_template('register_or_login.html')
    
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST' and 'profile_pic' in request.files:
        file = request.files['profile_pic']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Update the current user's profile_image field
            current_user.profile_image = filename
            db.session.commit()

            flash('Profile picture updated!', 'success')

    return render_template('profile.html')



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed due to {str(e)}", 'danger')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            # Redirect to a protected page or index after successful login
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    # Redirect to home page after logout
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET'])
def dashboard():

    bar_chart_json = create_bar_chart()

    # Select only numeric columns for the correlation matrix
    numeric_data = data.select_dtypes(include=[np.number])
    
    # Calculate the correlation matrix
    correlation_matrix = numeric_data.corr()

    # Create the heatmap
    heatmap = go.Figure(data=go.Surface(
        z=correlation_matrix.values, 
        x=correlation_matrix.columns, 
        y=correlation_matrix.index, 
        colorscale='Viridis'
    ))
    heatmap.update_layout(title='Correlation Matrix')
    # Convert the figure to JSON
    plotly_json = json.dumps(heatmap, cls=plotly.utils.PlotlyJSONEncoder)

    # Pass the JSON to the template
    return render_template('dashboard.html', plotly_json=plotly_json, bar_chart_json=bar_chart_json)

@app.context_processor
def inject_current_year():
    return {'current_time': datetime.utcnow()}



@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        # Extract form data from request and convert to appropriate types
        data = {
            'Property_Type': request.form.get('Property_Type'),
            'Property_Size': int(request.form.get('Property_Size')),
            'Bedrooms': int(request.form.get('Bedrooms')),
            'Bathrooms': int(request.form.get('Bathrooms')),
            'Location': request.form.get('Location'),
            'Furnishing': request.form.get('Furnishing'),
            'Age_of_Property': int(request.form.get('Age_of_Property')) if request.form.get('Age_of_Property') else None,
            'Amenities': request.form.get('Amenities'),
            'Proximity_to_Important_Locations': float(request.form.get('Proximity_to_Important_Locations')) if request.form.get('Proximity_to_Important_Locations') else None,
            'Floor_Level': int(request.form.get('Floor_Level')),
            'Property_Status': request.form.get('Property_Status')
        }

        # Make request to FastAPI for prediction
        response = requests.post(FASTAPI_ENDPOINT, json=data)
        prediction = response.json().get("predicted_price", None)
        return jsonify({'prediction': prediction})

    except Exception as e:
        flash(f"Prediction failed due to: {str(e)}", 'danger')
        return jsonify({'error': str(e)})

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        flash('Your account has been deleted!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting account: {str(e)}", 'danger')
    return redirect(url_for('index'))

@app.route('/remove_profile_image')
def remove_profile_image():
    # Logic to remove or reset current_user's profile_image
    current_user.profile_image = 'default.png'
    db.session.commit()
    return redirect(url_for('dashboard'))  # or wherever you want to redirect to

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
