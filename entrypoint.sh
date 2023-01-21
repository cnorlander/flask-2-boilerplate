#!/bin/bash
# Check python depenencies. Useful for development and autoupdating of dependencies on container reboot.
# If you find you have issues with dependency compatability you may want to remove this or set static version numbers in requirements.txt
echo "Checking Python Dependencies..."
pip3 install -r requirements.txt --root-user-action=ignore | grep -v 'already satisfied'

# Generate a self signed certificate for NGINX
chmod +x ./nginx/ssl/generate-selfsigned.sh
./nginx/ssl/generate-selfsigned.sh

# Boot the application with 5 workers using gthread workers. 
# Uses --reload to restart gunicorn. Might want to remove for production.
/usr/local/bin/gunicorn -b :8443 boilerplate:app --log-level=info --workers=5 -t 30 --worker-class=gthread --certfile=nginx/ssl/certificate.crt --keyfile=nginx/ssl/server.key --reload