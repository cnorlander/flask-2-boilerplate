#!/bin/bash
# Check python dependencies. Useful for development and auto updating of dependencies on container reboot.
# If you find you have issues with dependency compatibility you may want to remove this or set static version numbers in requirements.txt
echo "Checking Python Dependencies..."
pip3 install -r requirements.txt --root-user-action=ignore | grep -v 'already satisfied'

# Generate a self signed certificate for NGINX
chmod +x ./nginx/ssl/generate-selfsigned.sh
./nginx/ssl/generate-selfsigned.sh

# Boot the application with 5 workers using gthread workers. 
# Uses --reload to restart gunicorn. Might want to remove for production.
/usr/local/bin/gunicorn -b :8443 boilerplate:app --log-level=debug --workers=5 -t 30 --certfile=nginx/ssl/bundle.pem --keyfile=nginx/ssl/server.key --ssl-version=TLSv1_2 --reload