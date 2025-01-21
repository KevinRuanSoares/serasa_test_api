#!/bin/sh
# Check if the certificate exists, and if not, obtain it
if [ ! -d "/etc/letsencrypt/live/hom.model.api.kevinrsoares.com.br" ]; then
  certbot certonly --webroot -w /var/www/html/ -d hom.model.api.kevinrsoares.com.br --email contato@kevinrsoares.com.br --agree-tos --non-interactive

fi
# Renew the certificate
certbot renew --non-interactive --nginx
