# Softdesk : une API RESTful avec Django REST

## Objectif
Ce programme est un exercice proposé par [OpenClassRooms](https://openclassrooms.com/fr/) dans le cadre de la formation :
Développeur d'applications Python. L'objectif est de publier une application permettant de remonter et suivre des problèmes 
techniques, il s'agit d'un back-end performant et sécurisé, devant servir les applications sur toutes les plateformes (web, android, ios)

![logo](assets/logo.png)

## Fonctionnalités
L'application permet de :
* -> creer diverses projets
* -> d'ajouter des utilisateurs à des projets spécifiques
* -> de creer des problèmes au sein des projets
* -> d'ajouter des commentaires aux problèmes identifiés
* -> seuls les auteurs des projets, problèmes, commentaires peuvent les modifier ou les supprimer

## Technologie utilisée
* Le projet est développé avec le framework REST Django, il s'agit d'une API REST. 
* Les données sont sauvegardées dans une base de données sqlite3.
* Un swagger a été utilisé pour tester les points de terminaison de l'API et la documenter

## Installation
* Téléchargez et dézippez le repository github
* Creer l'environnement virtuel (exemple avec pipenv)
``` bash
mkdir .venv
pipenv install
pipenv shell
```

## Utilisation
* Lancer le serveur : `python manage.py runserver`
* Depuis votre navigateur habituel, l'accès à l'api se fait via l'url : `http:/127.0.0.1:8000`
* Pour creer un compte administrateur, utilisez la commande : `python manage.py createsuperuser`
* Pour accéder à l'administration : `http://127.0.0.1:8000/admin`
* Les endpoints peuvent êtres testés ici : `http://127.0.0.1:8000/schema`

## Documentation
* Vous pouvez accéder à la documentation de l'API ici : `http://127.0.0.1:8000/docs`


