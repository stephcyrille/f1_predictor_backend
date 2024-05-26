#!/bin/sh

# Remplace la variable ${SERVER_NAME} dans nginx.conf.template par la valeur de l'environnement
envsubst '${SERVER_NAME}' < /etc/nginx/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Exécute le serveur Nginx
nginx -g 'daemon off;'
