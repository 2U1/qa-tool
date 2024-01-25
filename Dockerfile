FROM python:3.12.1-bookworm

RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get install -y nodejs && \
    apt-get install -y npm

RUN python -m pip install --upgrade pip && \
    pip install fastapi 'uvicorn[standard]' && \
    pip install requests && \
    pip install pandas && \
    pip install pymongo && \
    pip install dnspython && \
    pip install motor && \
    pip install gunicorn && \
    pip install odmantic

RUN npm install svelte-spa-router