from flask.app import Flask
from werkzeug import datastructures
from wtforms.fields.simple import HiddenField, SubmitField
from .app import app, login_manager, db
from flask import render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, Email, URL, ValidationError
from website.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

def already_exist(form, field):
    if get_user_by_username(form.username.data) or get_user_by_email(form.email.data):
        raise ValidationError("Pseudo ou Email déjà pris")

def same_passwords(form, field):
    if form.password.data != form.password_confirmation.data:
        raise ValidationError("Les mots de passe ne correspondent pas")

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
                                               Length(max = 50, message = "L'Email ne doit pas faire plus de 50 caractères"),
                                               already_exist],
                                               id = "floatingInput", render_kw = {"placeholder": "baptiste@gmail.com"})
    
    username = StringField('Pseudo', validators = [InputRequired(message = "Le pseudo est obligatoire"), 
                                                   Length(min = 4, max = 15, message = "Le pseudo doit faire entre 4 et 15 caractères"),
                                                   already_exist], 
                                                   id = "floatingInput", render_kw = {"placeholder": "baptiste"})
    
    password = PasswordField('Mot de passe', validators = [InputRequired(message = "Le mot de passe est obligatoire"),
                                                           Length(min = 8, max = 80, message = "Le mot de passe doit faire entre 8 et 80 caractères")],
                                                           id = "floatingPassword", render_kw = {"placeholder": "Azerty20"})
    
    password_confirmation = PasswordField('Confirmer votre mot de passe', validators = [InputRequired(message = "Confirmation obligatoire"), same_passwords],
                                                           id = "floatingPassword", render_kw = {"placeholder": "Azerty20"})
    
    
    submit = SubmitField("S'inscrire")


class EditForm(FlaskForm):
    email = StringField("Email", validators = [InputRequired(message = "L'Email est obligatoire"),
                                               Email(message="Email invalide", check_deliverability = True),
                                               Length(max = 50, message = "L'Email ne doit pas faire plus de 50 caractères"),
                                               ],
                                               id = "floatingInput", render_kw = {"placeholder": "baptiste@gmail.com"})
    
    passwordL = PasswordField('Ancien mot de passe', validators = [InputRequired(message = "Le mot de passe est obligatoire"),
                                                           Length(min = 8, max = 80, message = "Le mot de passe doit faire entre 8 et 80 caractères")],
                                                           id = "floatingPassword", render_kw = {"placeholder": "Azerty20"})

    password = PasswordField('Mot de passe', validators = [InputRequired(message = "Le mot de passe est obligatoire"),
                                                           Length(min = 8, max = 80, message = "Le mot de passe doit faire entre 8 et 80 caractères")],
                                                           id = "floatingPassword", render_kw = {"placeholder": "Azerty20"})
    
    password_confirmation = PasswordField('Confirmer votre mot de passe', validators = [InputRequired(message = "Confirmation obligatoire"), same_passwords],
                                                           id = "floatingPassword", render_kw = {"placeholder": "Azerty20"})
    
    modify = SubmitField("Modifier")
    
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
    
    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = create_user(username = form.username.data, email = form.email.data, password = hashed_password, role_id = get_role_id("Utilisateur"))
        login_user(new_user, remember = False)
        return redirect(url_for("home"))

    
    return render_template(
        "register.html",
        form = form,
        user = current_user
    )
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

class SearchForm(FlaskForm):
    search = StringField(render_kw = {"placeholder": "Rechercher..."})
    submit = SubmitField("Rechercher")

@app.route("/", methods=['GET', 'POST'])
def home(): 
    page = request.args.get('page', 1, type=int)
    search = SearchForm()
    if search.validate_on_submit():
        animes = get_anime_by_filter(search.search.data, 1, 18)
    else:
        animes = get_animes_pagination(page, 18) 
    
    return render_template(
        "index.html",
        user = current_user,
        title = "My Anime Songs",
        animes = animes,
        form = search
    )

@app.route("/anime/<id>", methods=['GET', 'POST'])
def anime(id):

    favorites = []

    if current_user.is_authenticated:
        favorites = get_favorites_songs_of_user(get_user(current_user.id))

    return render_template(
        "anime.html",
        user = current_user,
        anime = get_anime(id),
        op = get_opening_by_anime_id(id),
        ed = get_ending_by_anime_id(id),
        ost = get_ost_by_anime_id(id),
        display = "all",
        favorites = favorites
    )

@app.route("/anime/<id>/opening", methods=['GET', 'POST'])
def anime_opening(id):
    return render_template(
        "anime.html",
        user = current_user,
        anime = get_anime(id),
        songs = get_opening_by_anime_id(id),
        display = "opening"
    )

@app.route("/anime/<id>/ending", methods=['GET', 'POST'])
def anime_ending(id):
    return render_template(
        "anime.html",
        user = current_user,
        anime = get_anime(id),
        songs = get_ending_by_anime_id(id),
        display = "ending"
    )

@app.route("/anime/<id>/ost", methods=['GET', 'POST'])
def anime_ost(id):
    return render_template(
        "anime.html",
        user = current_user,
        anime = get_anime(id),
        songs = get_ost_by_anime_id(id),
        display = "ost"
    )
    
def is_anime(form, field):
    if not get_anime_by_name(field.data):
        raise ValidationError("L'anime ne figure pas dans la base de données")
    
class RequestSongForm(FlaskForm):
    anime = StringField("Selectionnez un anime", validators = [InputRequired(message = "Champ obligatoire"), is_anime], render_kw = {"list": "datalistAnime"})
    title = StringField("Titre", validators = [InputRequired(message = "Champ obligatoire"), Length(max = 60)],
                        render_kw = {"placeholder": "Fly High!!"})
    interpreter = StringField("Interprète", validators = [InputRequired(message = "Champ obligatoire"), Length(max = 60, message = "Ne peux pas faire plus de 60 caractères")],
                              render_kw = {"placeholder": "BURNOUT SYNDROMES"})
    relation = StringField("Relation", validators = [InputRequired(message = "Champ obligatoire"), Length(max = 5, message = "Ne peux pas faire plus de 5 caractères")],
                           render_kw = {"placeholder": "OP2"})
    ytb_url = StringField("URL Youtube", validators = [InputRequired(message = "Champ obligatoire"), Length(max = 120, message = "Ne peux pas faire plus de 120 caractères")],
                          render_kw = {"placeholder": "https://www.youtube.com/watch?v=txgg-fbVjf4&ab_channel=BURNOUTSYNDROMESVEVO"})
    spoty_url = StringField("URL Spotify", validators = [InputRequired(message = "Champ obligatoire"), Length(max = 120, message = "Ne peux pas faire plus de 120 caractères")],
                             render_kw = {"placeholder": "https://open.spotify.com/track/3YOZLPRiTuYgItSGO41gPT?si=4e9a74511f334ef2"})
    submit = SubmitField("Envoyer la demande")
    
    # administration part
    
    accept = SubmitField("Accepter la demande")
    refuse = SubmitField("Rejeter la demande")
    modify = SubmitField("Modifier")
    delete = SubmitField("Supprimer")
        
@app.route("/request/song", methods=['GET', 'POST'])
@login_required
def request_song():
    
    form = RequestSongForm()

    form.anime.render_kw["value"] = ""
    form.title.render_kw["value"] = ""
    form.relation.render_kw["value"] = ""
    form.interpreter.render_kw["value"] = ""
    form.ytb_url.render_kw["value"] = ""
    form.spoty_url.render_kw["value"] = ""
    
    if form.validate_on_submit():
        
        create_song_request(
            title = form.title.data,
            interpreter = form.interpreter.data,
            relation = form.relation.data,
            ytb_url = form.ytb_url.data,
            spoty_url = form.spoty_url.data,
            anime_name = form.anime.data,
            user_id = current_user.id
        )
        
        return redirect(url_for("profile_request"))
    
    return render_template(
        "request-song.html",
        user = current_user,
        form = form,
        animes = get_animes()
    )
    
def anime_already_exist(form, field):
    for anime in get_animes():
        if anime.name == field.data:
            raise ValidationError("L'anime est déjà dans la base de données")

class RequestAnimeForm(FlaskForm):
    name = StringField("Nom", validators = [InputRequired(message = "Champ obligatoire"), Length(max = 80), anime_already_exist],
                        render_kw = {"placeholder": "Haikyuu - Saison 4"})
    img_url = StringField("URL d'une miniature", validators = [InputRequired(message = "Champ obligatoire"), Length(max = 120, message = "Ne peux pas faire plus de 120 caractères")],
                          render_kw = {"placeholder": "https://kbimages1-a.akamaihd.net/41c745b0-f165-4aa8-b2b1-f96cfdb6e594/353/569/90/False/haikyu-les-as-du-volley-chapitre-1.jpg"})
    text = TextAreaField("Description de l'anime", validators = [InputRequired(message= "Champ obligatoire"), Length(max = 1000)],
                          render_kw = {"placeholder": "Le héros meurt à la fin..."})
    submit = SubmitField("Envoyer la demande")
    
    # administration part

    accept = SubmitField("Accepter la demande")
    refuse = SubmitField("Rejeter la demande")
    modify = SubmitField("Modifier")
    delete = SubmitField("Supprimer")

class EditAnimeForm(FlaskForm):
    name = StringField("Nom", validators = [InputRequired(message = "Champ obligatoire"), Length(max = 80), is_anime],
                        render_kw = {"placeholder": "Haikyuu - Saison 4"})
    img_url = StringField("URL d'une miniature", validators = [InputRequired(message = "Champ obligatoire"), Length(max = 120, message = "Ne peux pas faire plus de 120 caractères")],
                          render_kw = {"placeholder": "https://kbimages1-a.akamaihd.net/41c745b0-f165-4aa8-b2b1-f96cfdb6e594/353/569/90/False/haikyu-les-as-du-volley-chapitre-1.jpg"})
    text = TextAreaField("Description de l'anime", validators = [InputRequired(message= "Champ obligatoire"), Length(max = 1000)],
                          render_kw = {"placeholder": "Le héros meurt à la fin..."})
    
    # administration part

    modify = SubmitField("Modifier")
    delete = SubmitField("Supprimer")

@app.route("/request/anime", methods=['GET', 'POST'])
@login_required
def request_anime():
    
    form = RequestAnimeForm()
    
    if request.method == 'POST':
        
        create_anime_request(
            name = form.name.data,
            img_url = form.img_url.data,
            user_id = current_user.id
        )
        
        return redirect(url_for("profile_request"))
    
    return render_template(
        "request-anime.html",
        user = current_user,
        form = form
    )

@app.route("/profile/request")
@login_required
def profile_request():
    
    return render_template(
        "profile-request.html",
        user = current_user,
        song_requests = get_song_requests_by_user(current_user),
        anime_requests = get_anime_requests_by_user(current_user)
    )

@app.route("/administration/request", methods = ['GET', 'POST'])
@login_required
def administration_request():
    
    if not current_user.role.name == "Administrateur":
        return redirect(url_for("home"))
    
    if request.method == "POST":
        print("salut")
        
    return render_template(
        "administration-request.html",
        user = current_user,
        song_requests = get_song_requests(),
        anime_requests = get_anime_requests()
    )
    
@app.route("/administration/request/song/<int:id>", methods = ['GET', 'POST'])
@login_required
def administration_request_song(id):
    
    if not current_user.role.name == "Administrateur":
        return redirect(url_for("home"))
    
    request = get_song_request(id)
        
    form = RequestSongForm()
    
    form.anime.render_kw["value"] = request.anime.name
    form.title.render_kw["value"] = request.title
    form.relation.render_kw["value"] = request.relation
    form.interpreter.render_kw["value"] = request.interpreter
    form.ytb_url.render_kw["value"] = request.ytb_url
    form.spoty_url.render_kw["value"] = request.spoty_url
    
    if form.validate_on_submit():
        
        if form.accept.data :

            create_song(
                title = form.title.data,
                interpreter = form.interpreter.data,
                relation = form.relation.data,
                ytb_url = form.ytb_url.data,
                spoty_url = form.spoty_url.data,
                anime_id = get_anime_by_name(form.anime.data).id
            )
            
            set_status(request, "Acceptée")
            
        else :
            
            set_status(request, "Rejetée")
        
        return redirect(url_for("administration_request"))
        
    return render_template(
        "administration-request-song.html",
        user = current_user,
        request = request,
        form = form
    )
    
@app.route("/administration/request/song/<int:id>/delete", methods = ['GET', 'POST'])
@login_required
def administration_request_song_delete(id):
    
    if not current_user.role.name == "Administrateur":
        return redirect(url_for("home"))
    
    request = get_song_request(id)
    
    if request:
        delete_request(request)
    
    return redirect(url_for("administration_request"))

@app.route("/profile/request/song/<int:id>/delete", methods = ['GET', 'POST'])
@login_required
def profile_request_song_delete(id):
    
    request = get_song_request(id)
    
    if request:
        if request in get_song_requests_by_user(current_user):
            delete_request(request)
    
    return redirect(url_for("profile_request"))

@app.route("/profile/request/anime/<int:id>/delete", methods = ['GET', 'POST'])
@login_required
def profile_request_anime_delete(id):
    
    request = get_anime_request(id)
    
    if request:
        if request in get_anime_requests_by_user(current_user):
            delete_request(request)
    
    return redirect(url_for("profile_request"))

@app.route("/administration/request/anime/<int:id>", methods = ['GET', 'POST'])
@login_required
def administration_request_anime(id):
    
    if not current_user.role.name == "Administrateur":
        return redirect(url_for("home"))
    
    request = get_anime_request(id)
        
    form = RequestAnimeForm()
    
    form.name.render_kw["value"] = request.name
    form.img_url.render_kw["value"] = request.img_url
    
    if form.validate_on_submit():
        
        if form.accept.data:

            create_anime(
                name = form.name.data
            )
            
            set_status(request, "Acceptée")
            
        else :
            
            set_status(request, "Rejetée")
        
        return redirect(url_for("administration_request"))
        
    return render_template(
        "administration-request-anime.html",
        user = current_user,
        request = request,
        form = form
    )
    
@app.route("/administration/request/anime/<int:id>/delete", methods = ['GET', 'POST'])
@login_required
def administration_request_anime_delete(id):
    
    if not current_user.role.name == "Administrateur":
        return redirect(url_for("home"))
    
    request = get_anime_request(id)
    
    if request:
        delete_request(request)
    
    return redirect(url_for("administration_request"))


@app.route("/administration/edit/song/<int:id>", methods = ['GET', 'POST'])
@login_required
def administration_edit_song(id):

    if not current_user.role.name == "Administrateur":
        return redirect(url_for("home"))

    song = get_song(id)
        
    form = RequestSongForm()
    
    form.anime.render_kw["value"] = song.anime.name
    form.title.render_kw["value"] = song.title
    form.relation.render_kw["value"] = song.relation
    form.interpreter.render_kw["value"] = song.interpreter
    form.ytb_url.render_kw["value"] = song.ytb_url
    form.spoty_url.render_kw["value"] = song.spoty_url
    
    if form.validate_on_submit():
        if form.modify.data:
            edit_song(
                form.title.data,
                form.interpreter.data,
                form.relation.data,
                form.ytb_url.data,
                form.spoty_url.data,
                song
            )

        return redirect(url_for("home"))
    
    return render_template(
        "administration-edit-song.html",
        user = current_user,
        song = song,
        form = form
    )


@app.route("/administration/edit/anime/<int:id>", methods = ['GET', 'POST'])
@login_required
def administration_edit_anime(id):
    
    if not current_user.role.name == "Administrateur":
        return redirect(url_for("home"))

    anime = get_anime(id)

    form = EditAnimeForm()

    form.name.render_kw["value"] = anime.name
    form.img_url.render_kw["value"] = anime.img
    form.text.render_kw["value"] = anime.text

    if form.validate_on_submit():
        if form.modify.data:
            edit_anime(
                form.img_url.data,
                form.text.data,
                anime
            )

        return redirect(url_for("home"))

    return render_template(
        "administration-edit-anime.html",
        user = current_user,
        anime = anime,
        form = form
    )

@app.route("/profile/favorites")
@login_required
def profile_favorites():

    return render_template(
        "profile-favorites.html",
        user = current_user,
        favorites = get_favorites_of_user(get_user(current_user.id))
    )

@app.route("/profile/settings", methods = ['GET', 'POST'])
@login_required
def profile_settings():

    userEdit = get_user(current_user.id)

    form = EditForm()
    form.email.render_kw["value"] = userEdit.email

    if form.validate_on_submit():
        if check_password_hash(userEdit.password, form.passwordL.data):
            if form.modify.data:
                hashed_password = generate_password_hash(form.password.data, method="sha256")
                edit_user(email = form.email.data, password = hashed_password, userEdit = userEdit)
                return redirect(url_for("home"))

    return render_template(
        "profile-settings.html",
        user = current_user,
        form = form,
        userEdit = userEdit
    )
        
@app.route("/songs/all/", methods = ['GET', 'POST'])
def songs():
    page = request.args.get('page', 1, type=int)
    tri = request.args.get('tri', None, type=int)
    search = SearchForm()
    if tri == 1:
        songs = get_songs_by_name_pagination_ascendant(page, 48)
    elif tri == 2:
        songs = get_songs_by_name_pagination_descendant(page, 48)
    elif tri == 3:
        songs = get_op(page, 48)
    elif tri == 4:
        songs = get_ed(page, 48)
    elif tri == 5:
        songs = get_ost(page, 48)
    if search.validate_on_submit():
        songs = get_song_by_filter(search.search.data, 1, 48)
    elif not tri:
        songs = get_songs_pagination(page, 48)
    return render_template(
        "songs.html",
        user = current_user,
        songs = songs,
        form = search
    )
    
@app.route("/anime/<int:id_a>/add/<int:id>", methods = ['GET', 'POST'])
@login_required
def profile_favorites_add(id_a, id):
    add_favorite(current_user.id, id)
    return redirect(url_for("anime", id = id_a))

@app.route("/anime/<int:id_a>/delete/<int:id>", methods = ['GET', 'POST'])
@login_required
def profile_favorites_remove(id_a, id):
    remove_favorite(current_user.id, id)
    return redirect(url_for("anime", id = id_a))

@app.route("/animes/all/", methods = ['GET', 'POST'])
def animes():
    page = request.args.get('page', 1, type=int)
    search = SearchForm()
    if search.validate_on_submit():
        animes = get_anime_by_filter(search.search.data, 1, 48)
    else:
        animes = get_animes_pagination(page, 48) 
    return render_template(
        "animes.html",
        user = current_user,
        animes = animes,
        form = search
    )

@app.route("/anime/<int:id_a>/song/<int:id>/delete", methods = ['GET', 'POST'])
@login_required
def song_delete(id_a, id):

    if not current_user.role.name == "Administrateur":
        return redirect(url_for("anime", id = id_a))

    remove_song(id)
    return redirect(url_for("anime", id = id_a))

@app.route("/anime/<int:id>/delete", methods = ['GET', 'POST'])
@login_required
def anime_delete(id):

    if not current_user.role.name == "Administrateur":
        return redirect(url_for("home"))

    remove_anime(id)
    return redirect(url_for("home"))