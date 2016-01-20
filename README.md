[![Build Status](https://travis-ci.org/BinetReseau/chocapix-server.svg?branch=develop)](https://travis-ci.org/BinetReseau/chocapix-server)
[![Coverage Status](https://coveralls.io/repos/BinetReseau/chocapix-server/badge.svg?branch=develop&service=github)](https://coveralls.io/github/BinetReseau/chocapix-server?branch=develop)

# API REST pour Chocapix

Ce projet est l'API REST du site des bars d'étages.  
Il est conçu avec le framework web [Django 1.8](https://www.djangoproject.com/) et utilise très largement le package [Django REST Framework](http://http://www.django-rest-framework.org/).

## Installation rapide
L'application requiert Python 2.7. On utilise `pip` pour la gestion des dépendances.
```shell
pip install -r requirements.txt
./resetdb.sh
python manage.py runserver
```
Plus de détails sont donnés [sur le wiki](https://github.com/BinetReseau/chocapix-server/wiki).

## Documentation
Le fonctionnement général du projet et le détail de chaque application sont expliqués [dans le wiki](https://github.com/BinetReseau/chocapix-server/wiki).

L'API interactive du Django REST Framework est accessible à l'adresse `http://127.0.0.1:8000/` (lorsque le serveur de développement de Django est lancé).

De plus, une API interactive plus complète est disponible à l'adresse `http://127.0.0.1:8000/docs/`.
