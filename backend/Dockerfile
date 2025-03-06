FROM python:3.13-slim-bookworm

RUN apt-get update
RUN apt-get -y upgrade

ARG NEXT_PUBLIC_BUILD_VERSION="undefined"
ENV PYTHONPATH=/app/api
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
COPY api ./api
COPY tests ./tests
RUN echo $NEXT_PUBLIC_BUILD_VERSION > ./api/__version__

CMD [ "gunicorn", "--bind", "0.0.0.0:8080", "-w", "4", "wsgi", "--access-logfile",  "-"]
