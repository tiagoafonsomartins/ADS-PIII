# ADS-PIII

# Informação sobre o dockerfile
Para correr no Docker, pode-se correr via a imagem situada no Hub: 
https://hub.docker.com/r/saltedcookie/ads-piii

De seguida, é necessário indicar, na CLI, os seguintes comandos:
python ADS-PIII/manage.py migrate 
python ADS-PIII/manage.py runserver 0.0.0.0:8000
