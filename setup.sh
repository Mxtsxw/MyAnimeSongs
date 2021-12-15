#!/bin/bash
read -p "voulez vous (re)créer le virtualenv ?[y/n]" reponse
if echo "$reponse" | grep -iq "^y" ;then
    rm -rf venv
    virtualenv -p python3 venv
    echo "Environnement créé"
fi

source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=./app.py
export FLASK_DEBUG=1

echo -e "-------------------------------------\nsource venv/bin/activate"
