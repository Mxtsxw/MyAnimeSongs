from flask.app import Flask
from wtforms.fields.simple import HiddenField, SubmitField
from .app import app, login_manager
from flask import render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, Email
from website.models import get_anime, get_animes, get_song, get_songs, get_songs_anime
from .models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    submit = SubmitField("Sign in")
    
class RegisterForm(FlaskForm):
    email = StringField("email", validators=[InputRequired(), Email(message="Invalid email", check_deliverability=True), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField("Sign up")
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                return redirect(url_for("home"))
        
        return '<h1>Invalid username or password</h1>'
        
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    
    return render_template(
        "login.html",
        form = form
    )
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return "<h1>New User have been created</h1>"
        
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    
    return render_template(
        "register.html",
        form = form
    )
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
@login_required
def home():
    
    return render_template(
        "index.html",
        current_user.is_authenticated,
        title="My Anime Songs",
        animes = get_animes()
    )