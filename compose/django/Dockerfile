FROM python:3.6-alpine3.7

ENV PYTHONUNBUFFERED 1

COPY ./Pipfile* /

RUN apk add --no-cache bash ca-certificates wget shadow build-base python3-dev postgresql-dev \
    && wget https://s3.amazonaws.com/rds-downloads/rds-ca-2015-root.pem -P /usr/local/share/ca-certificates/ \
    && mv /usr/local/share/ca-certificates/rds-ca-2015-root.pem /usr/local/share/ca-certificates/rds-ca-2015-root.crt \
    && update-ca-certificates \
    && pip install pipenv \
    && pipenv install --system \
    && apk del --purge build-base python3-dev \
    && groupadd -r django \
    && useradd -r -g django django

COPY . /app
RUN chown -R django /app

COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
