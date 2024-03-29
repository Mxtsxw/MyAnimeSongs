# MyAnimeSongs

Projet d'ambition de recensemment de bande son d'animes. 

## Getting started

Afin de lancer le site en local sur un système d'exploitation Linux, il vous suffit de taper les commandes suivante.

## Lancement du projet (premier lancement)

```
git clone https://gitlab.com/Matsew/myanimesongs.git
cd ./myanimesongs/
./setup.sh
source venv/bin/activate
flask create-db
flask run
```

Une fois le server lancé en local, le site est accessible à l'url suivant :

> http://localhost:5000/

## Lancement du projet (simple)

Dans le cas où le projet a déjà été lancé, la suite d'instructions suivante suffit 

```
source venv/bin/activate
flask run
```

## Dépendances

Dans le cas où les modules ne peuvent pas être installé automatiquement à l'aide du script, voici la liste des modules nécessaires.

> pyyaml
> flask
> flask-dotenv
> flask-bootstrap5
> flask-sqlalchemy
> flask-wtf
> flask-login
> flask-marshmallow
> marshmallow-sqlalchemy
> flask-cors
> flask-dotenv

*Pour plus de détails, se référer au fichier requirement.txt*

## API REST

Nous mettons à disposition une API pour intéragir avec l'application. 
Les requêtes prennent la forme suivante : `api/[ressource]/<id>`

Voici une liste des endpoints disponibles :
![Endpoints POSTMAN](https://user-images.githubusercontent.com/85303770/221856304-66c13f28-3e2c-4a47-b987-cb5c8efe933a.png)

Pour plus d'information le code source est disponible dans le projet [api.py](https://github.com/Mxtsxw/MyAnimeSongs/blob/main/website/api.py).


## Screenshots 

![Screenshot 1](https://user-images.githubusercontent.com/85303770/212152681-6f8dd8ba-6d78-4d75-b261-fcc7d11a59c9.jpg)


## CRÉDITS

Projet réalisé par **Matthieu RANDRIANTSOA**, Baptiste LAMBERT et François ZHU.
