FROM python:3.12.1-bookworm

COPY qa /etc/nginx/sites-available/qa

RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get install -y nodejs && \
    apt-get install -y npm

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

RUN npm install -g svelte-spa-router && \
    npm install -g bootstrap && \
    npm install -g moment && \
    npm install -g qs

RUN rm /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/qa /etc/nginx/sites-enabled/qa