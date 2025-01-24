FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="kevinrsoares.com.br"

# Copy necessary files
COPY ./options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh
COPY ./renew-certificate.sh /renew-certificate.sh
COPY ./generate-dhparam.sh /generate-dhparam.sh


# Environment variables
ENV LISTEN_PORT=80
ENV SSL_LISTEN_PORT=443
ENV APP_HOST=app
ENV APP_PORT=9000

# Switch to root user to perform privileged operations
USER root

# Directory setup and permission adjustments
RUN mkdir -p /vol/static && \
    chmod -R 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    mkdir -p /var/log/letsencrypt && \
    chown -R nginx:nginx /var/log/letsencrypt && \
    chmod -R 755 /var/log/letsencrypt && \
    mkdir -p /var/lib/letsencrypt && \
    chown -R nginx:nginx /var/lib/letsencrypt && \
    chmod -R 755 /var/lib/letsencrypt && \
    mkdir -p /etc/letsencrypt/ && \
    chown -R nginx:nginx /etc/letsencrypt/ && \
    chmod -R 755 /etc/letsencrypt/ && \
    mkdir -p /var/www/html && \
    chown -R nginx:nginx /var/www/html && \
    chmod -R 755 /var/www/html && \
    touch /etc/letsencrypt/.certbot.lock && \
    chown nginx:nginx /etc/letsencrypt/.certbot.lock && \
    chmod +x /run.sh && \
    chmod +x /renew-certificate.sh && \
    chmod +x /generate-dhparam.sh

# Install necessary packages
RUN apk add --no-cache certbot py3-pip openssl && \
    pip install certbot-nginx --break-system-packages

# Switch back to nginx user
USER nginx

# Define volumes
VOLUME /vol/static
VOLUME /etc/letsencrypt
VOLUME /var/www/html

# Set the command to run
CMD ["/run.sh"]
