# Rasa - TP
## Le but de ce chatbot est de pouvoir prendre des réservations

### Comment lancer l'interface

Dans deux terminals différents, lancer ces deux commandes :

    python -m http.server #interface graphique

    rasa run --enable-api --cors="*" #modele rasa

### Entrainement du modèle

Il faut lancer Duckling en local avant d'entrainer son modèle

docker run -p 8000:8000 rasa/duckling

Entrainer le modèle : 

rasa train


    
