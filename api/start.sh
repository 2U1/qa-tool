#!/bin/bash
# entrypoint.sh
cd /home/workspace/api

# Start nginx service
service nginx start

# Then start your main application
exec gunicorn main:app \
      --workers 6 \
      --worker-class uvicorn.workers.UvicornWorker \
      --bind unix:/tmp/qa.sock \
      --log-config /home/workspace/api/logs/uvicorn_log.ini