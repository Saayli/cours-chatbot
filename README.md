# Rasa - TP
## Le but de ce chatbot est de pouvoir prendre des réservations

### Comment lancer le bot

Il suffit de lancer le script à la racine : lancer_rasa.sh

Quand il est écrit : *Rasa server is up and running*. Vous pouvez commencer à chatter avec le bot.
### Entrainement du modèle

Entrainer le modèle : 

rasa train

### Conversation fonctionnelle
#### Réserver une table
![image](https://github.com/user-attachments/assets/e4fcc535-12d5-48b0-928e-452c93167f74)

#### Checker une réservation
![image](https://github.com/user-attachments/assets/81f04241-7f97-4bab-b096-d05250ba54a4)

### Démarche

Quentin a commencer par générer un parcours puis les stories à l'aide de ChatGpt
Parallèlement, Ilyas à implémenter l'interface graphique.

Ensemble nous avons implémenter les actions et essayer de les faire fonctionner.

Le problème était que le bot comprenait parfois les bons intents mais pourtant ne réagissait pas comme nous le voulions.
Ce qui nous a obliger à utiliser les rules. Ce que je trouve: pas du tout optimal. Par exemple on a le check et l'annulation de la réservation qui fonctionne, mais impossible de faire fonctionner les deux à causes des rules.
On a essayé de modifié la config mais sans succès.

On a fait fonctionner le formulaire ce qui permet de faire des erreurs dans les réponses sans recommencer de zéro la réservation.


    
