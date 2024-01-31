FROM python:3.12.1-bookworm

COPY qa /etc/nginx/sites-available/qa

RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get install -y nodejs && \
    apt-get install -y npm

RUN python -m pip install --upgrade pip && \
    pip install fastapi 'uvicorn[standard]' && \
    pip install pymongo && \
    pip install dnspython && \
    pip install motor && \
    pip install gunicorn && \
    pip install 'passlib[bcrypt]' && \
    pip install bcrypt==4.0.1 && \
    pip install python-multipart && \
    pip install "python-jose[cryptography]" && \
    pip install pytz

RUN npm install -g svelte-spa-router && \
    npm install -g bootstrap && \
    npm install -g moment && \
    npm install -g qs

RUN rm /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/qa /etc/nginx/sites-enabled/qa