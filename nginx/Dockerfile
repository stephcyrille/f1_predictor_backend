FROM nginx:latest

# Copier le fichier modèle nginx.conf.template
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Copier le script d'entrée
COPY entrypoint.sh /entrypoint.sh

# Assurer l'exécution du script d'entrée
RUN chmod +x /entrypoint.sh

# Définir le script d'entrée comme point d'entrée
ENTRYPOINT ["/entrypoint.sh"]
