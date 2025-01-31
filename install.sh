#!/bin/bash
# takes two paramters, the domain name and the email to be associated with the certificate
DOMAIN=$1
EMAIL=$2

echo Creating .env file...

echo POSTGRES_DB=treescope >> .env
echo POSTGRES_USER=treescope-user >> .env
echo POSTGRES_PASSWORD=$(openssl rand 60 | base64 -w 0) >> .env
echo SECRET_KEY=$(openssl rand 60 | base64 -w 0) >> .env
echo DOMAIN="${DOMAIN}" >> .env
echo EMAIL="${EMAIL}" >> .env


# Phase 1
echo Installing SSL certificates...
sudo docker compose -f ./compose-initiate.yaml up -d nginx
sudo docker compose -f ./compose-initiate.yaml up certbot
sudo docker compose -f ./compose-initiate.yaml down

# some configurations for let's encrypt
echo Configuring let\'s encrypt...
curl -L --create-dirs -o etc/letsencrypt/nginx/options-ssl-nginx.conf https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf
openssl dhparam -out etc/letsencrypt/nginx/ssl-dhparams.pem 2048

# Phase 2
echo Installing cron job...
sudo crontab ./etc/cron/crontab
echo Starting containers...
sudo docker compose -f ./compose.yaml up -d