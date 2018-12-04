FROM python:3.6-alpine3.6

RUN apk update
RUN apk upgrade
RUN apk add bash

ENV PYTHONPATH=/app/missal1962
WORKDIR /app

COPY Pipfile* ./
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

RUN mkdir -pv \
             resources/divinum-officium/web/www/missa/Polski \
             resources/divinum-officium/web/www/missa/Latin
COPY resources/divinum-officium/web/www/missa/Polski ./resources/divinum-officium/web/www/missa/Polski
COPY resources/divinum-officium/web/www/missa/Latin ./resources/divinum-officium/web/www/missa/Latin
COPY resources/divinum-officium-custom ./resources/divinum-officium-custom
COPY missal1962 ./missal1962
COPY deploy.sh .
RUN ./deploy.sh

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "wsgi"]
