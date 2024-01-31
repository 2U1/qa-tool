#!/bin/bash
# stop_gunicorn.sh

# Send TERM signal to gracefully stop Gunicorn
pkill -f 'gunicorn'

# Send QUIT signal to gracefully stop nginx
service nginx stop