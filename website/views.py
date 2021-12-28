from flask.app import Flask
from wtforms.fields.simple import HiddenField, SubmitField
from .app import app, login_manager
from flask import render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, Email
from website.models import get_anime, get_animes, get_song, get_songs, get_songs_anime
from .models import db, User, Role
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


class LoginForm(FlaskForm):
    username = StringField('Pseudo', validators = [InputRequired(message = "Le pseudo est obligatoire"), 
                                                   Length(min = 4, max = 15, message = "Le pseudo doit faire entre 4 et 15 caractères")], 
                                                   id = "floatingInput", render_kw = {"placeholder": "baptiste"})
    
    password = PasswordField('Mot de passe', validators = [InputRequired(message = "Le mot de passe est obligatoire"),
                                                           Length(min = 8, max = 80, message = "Le mot de passe doit faire entre 8 et 80 caractères")],
                                                           id = "floatingPassword", render_kw = {"placeholder": "Azerty20"})
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField("Se connecter")
    
class RegisterForm(FlaskForm):
    email = StringField("Email", validators = [InputRequired(message = "L'Email est obligatoire"),
                                               Email(message="Email invalide", check_deliverability = True),
                                               Length(max = 50, message = "L'Email ne doit pas faire plus de 50 caractères")],
                                               id = "floatingInput", render_kw = {"placeholder": "baptiste@gmail.com"})
    
    username = StringField('Pseudo', validators = [InputRequired(message = "Le pseudo est obligatoire"), 
                                                   Length(min = 4, max = 15, message = "Le pseudo doit faire entre 4 et 15 caractères")], 
                                                   id = "floatingInput", render_kw = {"placeholder": "baptiste"})
    
    password = PasswordField('Mot de passe', validators = [InputRequired(message = "Le mot de passe est obligatoire"),
                                                           Length(min = 8, max = 80, message = "Le mot de passe doit faire entre 8 et 80 caractères")],
                                                           id = "floatingPassword", render_kw = {"placeholder": "Azerty20"})
    
    password_confirmation = PasswordField('Confirmer votre mot de passe', validators = [InputRequired(message = "Confirmation obligatoire")],
                                                           id = "floatingPassword", render_kw = {"placeholder": "Azerty20"})
    
    submit = SubmitField("S'inscrire")
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    valid = True
    
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                return redirect(url_for("home"))
        
        valid = False
    
    return render_template(
        "login.html",
        valid = valid,
        form = form,
        user = current_user
    )
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    valid = True
    error_message = None
    
    if form.validate_on_submit():
        
        if User.query.filter_by(username = form.username.data).first() or User.query.filter_by(email = form.email.data).first():
            error_message = "Pseudo ou Email déjà pris"
            
        elif form.password.data != form.password_confirmation.data:
            error_message = "Les mots de passe ne correspondent pas"
        
        else:
            hashed_password = generate_password_hash(form.password.data, method="sha256")
            user_role_id = Role.query.filter_by(name = "Utilisateur").first().id
            new_user = User(username = form.username.data, email = form.email.data, password = hashed_password, role_id = user_role_id)
            db.session.add(new_user)
            db.session.commit()
        
            login_user(new_user, remember = False)
            return redirect(url_for("home"))

        valid = False
    
    return render_template(
        "register.html",
        valid = valid,
        error_message = error_message,
        form = form,
        user = current_user
    )
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
#@login_required
def home():
    
    return render_template(
        "index.html",
        user = current_user,
        title = "My Anime Songs",
        animes = get_animes()
    )