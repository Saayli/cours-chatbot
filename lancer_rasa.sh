#!/bin/bash

loading_bar() {
    local duration=${1:-5}
    local i=0
    local spin='-\|/'
    echo -n "Chargement : "
    while [ $i -lt $duration ]; do
        printf "\b${spin:i++%${#spin}:1}"
        sleep 0.2
    done
    echo
}

# Étape 1 : Entraînement de Rasa
echo "Étape 1 : Entraînement de Rasa (rasa train)"
loading_bar 5
rasa train

# Étape 2 : Lancement du serveur d’actions
echo
echo "Étape 2 : Lancement du serveur d’actions (rasa run actions)"
loading_bar 3
rasa run actions --actions actions --port 5055 &

# On donne un petit délai pour que le serveur d’actions soit opérationnel
sleep 3

# Étape 3 : Lancement du serveur HTTP pour l’UI
echo
echo "Étape 3 : Lancement du serveur HTTP (python -m http.server)"
loading_bar 2
python3 -m http.server 8000 &

# Étape 4 : Lancement de Rasa Server avec API et CORS
echo
echo "Étape 4 : Lancement de Rasa Server (API + CORS)"
loading_bar 3
rasa run --enable-api --cors="*" --endpoints endpoints.yml
