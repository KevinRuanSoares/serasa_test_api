#!/bin/sh

set -e

sh /generate-dhparam.sh
sh /renew-certificate.sh
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'