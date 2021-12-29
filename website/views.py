from flask.app import Flask
from wtforms.fields.simple import HiddenField, SubmitField
from .app import app, login_manager
from flask import render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, Email
from website.models import get_anime, get_animes, get_song, get_songs, get_songs_anime, get_role_id, get_user, get_user_by_username, get_user_by_email, create_user
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
    return get_user(user_id)
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    valid = True
    
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
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
        
        if get_user_by_username(form.username.data) or get_user_by_email(form.email.data):
            error_message = "Pseudo ou Email déjà pris"
            
        elif form.password.data != form.password_confirmation.data:
            error_message = "Les mots de passe ne correspondent pas"
        
        else:
            hashed_password = generate_password_hash(form.password.data, method="sha256")
            new_user = create_user(username = form.username.data, email = form.email.data, password = hashed_password, role_id = get_role_id("Utilisateur"))
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

@app.route("/anime/name")
def anime():
    return render_template(
        "anime.html",
        user = current_user,
    )