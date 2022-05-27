FROM python:3.9-slim-buster

RUN apt-get update
RUN apt-get -y upgrade

ENV PYTHONPATH=/app/missalemeum
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN mkdir -pv \
             resources/divinum-officium/web/www/missa/Latin \
             resources/divinum-officium/web/www/missa/English \
             resources/divinum-officium/web/www/missa/Polski
COPY resources/divinum-officium/web/www/missa/Latin ./resources/divinum-officium/web/www/missa/Latin
COPY resources/divinum-officium/web/www/missa/English ./resources/divinum-officium/web/www/missa/English
COPY resources/divinum-officium/web/www/missa/Polski ./resources/divinum-officium/web/www/missa/Polski
COPY resources/ordo ./resources/ordo
COPY resources/propers ./resources/propers
COPY resources/supplement ./resources/supplement
COPY resources/divinum-officium-custom ./resources/divinum-officium-custom
COPY missalemeum ./missalemeum
COPY tests ./tests

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "-w", "4", "wsgi"]
