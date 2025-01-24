server {
    listen ${LISTEN_PORT};
    server_name brain_agriculture.kevinsoares.com.br;

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

