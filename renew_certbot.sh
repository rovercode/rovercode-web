
se run --rm --name certbot certbot bash -c "sleep 6 && certbot certonly --standalone -d {{ cookiecutter.domain_name }} --text --agree-tos --email {{ cookiecutter.email }} --server https://acme-v01.api.letsencrypt.org/directory --rsa-key-size 4096 --verbose --keep-until-expiring --standalone-supported-challenges http-01"
docker exec pearl_nginx_1 nginx -s reload
