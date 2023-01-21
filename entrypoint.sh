./nginx/ssl/generate-selfsigned.sh
/usr/local/bin/gunicorn -b :8080 flask-boilerplate:app --log-level=info --workers=5 -t 30 --worker-class=gthread --reload