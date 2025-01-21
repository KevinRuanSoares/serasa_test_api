server {
    listen ${LISTEN_PORT};
    server_name hom.model.api.kevinrsoares.com.br;

    location /static {
        alias /vol/static;
    }

    location /.well-known/acme-challenge/ {
        root /var/www/html;
        allow all;
    }

    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    20M;
    }
}

server {
    listen ${SSL_LISTEN_PORT} ssl;
    server_name hom.model.api.kevinrsoares.com.br;

    ssl_certificate /etc/letsencrypt/live/hom.model.api.kevinrsoares.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hom.model.api.kevinrsoares.com.br/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    location /static {
        alias /vol/static;
    }
    location /.well-known/acme-challenge/ {
        root /var/www/html;
        allow all;
    }
    
    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    20M;
    }
}