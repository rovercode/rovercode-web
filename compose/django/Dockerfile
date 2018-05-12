FROM python:3.5

ENV PYTHONUNBUFFERED 1

RUN apt-get install -y ca-certificates wget \
    && wget https://s3.amazonaws.com/rds-downloads/rds-ca-2015-root.pem -P /usr/local/share/ca-certificates/ \
    && mv /usr/local/share/ca-certificates/rds-ca-2015-root.pem /usr/local/share/ca-certificates/rds-ca-2015-root.crt \
    && update-ca-certificates

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./Pipfile* /

RUN pip install pipenv && \
    pipenv install --system \
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
