#!/bin/bash
read -p "voulez vous (re)créer le virtualenv ?[y/n]" reponse
if echo "$reponse" | grep -iq "^y" ;then
    rm -rf venv
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements.txt
    echo "Environnement créé"
fi

export FLASK_APP=website

echo -e "-------------------------------------\nsource venv/bin/activate"
