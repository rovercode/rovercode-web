FROM python:3.8-alpine3.12

ENV PYTHONUNBUFFERED 1

COPY ./Pipfile* /

RUN apk add --no-cache bash ca-certificates wget shadow build-base python3-dev postgresql-dev libffi-dev libressl-dev \
    && wget https://s3.amazonaws.com/rds-downloads/rds-ca-2015-root.pem -P /usr/local/share/ca-certificates/ \
    && mv /usr/local/share/ca-certificates/rds-ca-2015-root.pem /usr/local/share/ca-certificates/rds-ca-2015-root.crt \
    && update-ca-certificates \
    && pip install --upgrade pip \
    && pip install pipenv==2018.11.26 \
    && pipenv install --ignore-pipfile --system \
    && apk del --purge build-base python3-dev \
    && groupadd -r django \
    && useradd -r -g django django

COPY . /app
RUN chown -R django /app

COPY ./compose/django/start.sh /start.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /start.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /start.sh \
    && chown django /start.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
