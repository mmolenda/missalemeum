FROM python:3.13-slim-bookworm

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y --no-install-recommends \
    libcairo2 \
    pango1.0-tools \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi8 \
    libxml2 \
    libxslt1.1 \
    libjpeg62-turbo \
    fonts-liberation \
    fonts-dejavu-core \
    shared-mime-info \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ARG NEXT_PUBLIC_BUILD_VERSION="undefined"
ENV PYTHONPATH=/app/api:/app
WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN mkdir -pv \
             resources/divinum-officium/web/www/missa/Latin \
             resources/divinum-officium/web/www/missa/English \
             resources/divinum-officium/web/www/missa/Polski \
             resources/divinum-officium/web/www/horas/Latin/Commune \
             resources/divinum-officium/web/www/horas/English/Commune \
             resources/divinum-officium/web/www/horas/Polski/Commune 
COPY resources/divinum-officium/web/www/missa/Latin ./resources/divinum-officium/web/www/missa/Latin
COPY resources/divinum-officium/web/www/missa/English ./resources/divinum-officium/web/www/missa/English
COPY resources/divinum-officium/web/www/missa/Polski ./resources/divinum-officium/web/www/missa/Polski
COPY resources/divinum-officium/web/www/horas/Latin/Commune ./resources/divinum-officium/web/www/horas/Latin/Commune
COPY resources/divinum-officium/web/www/horas/English/Commune ./resources/divinum-officium/web/www/horas/English/Commune
COPY resources/divinum-officium/web/www/horas/Polski/Commune ./resources/divinum-officium/web/www/horas/Polski/Commune

COPY resources/ordo ./resources/ordo
COPY resources/propers ./resources/propers
COPY resources/supplement ./resources/supplement
COPY resources/divinum-officium-local ./resources/divinum-officium-local
COPY api ./api
COPY pdf ./pdf
COPY tests ./tests
RUN echo $NEXT_PUBLIC_BUILD_VERSION > ./api/__version__

CMD [ "gunicorn", "--bind", "0.0.0.0:8080", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "api.app:app", "--access-logfile", "-" ]
