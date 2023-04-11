#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
KEY_FILE="${SCRIPT_DIR}/server.key"
CERT_FILE="${SCRIPT_DIR}/certificate.crt"
CERT_BUNDLE="${SCRIPT_DIR}/bundle.pem"
CSR_FILE="${SCRIPT_DIR}/signing-request.csr"


if [ ! -f $CERT_FILE ] && [ ! -f $KEY_FILE ] && [ ! -f $CERT_BUNDLE ]; 
    then
        echo "Certifcate Not Found: Generating Self Signed Certificate..."
        openssl req -nodes -newkey rsa:2048 -keyout $KEY_FILE -out $CSR_FILE -subj "/C=US/ST=Confusion/L=Lavender Town/O=Flask Nerds/OU=Certainly a Real Department/CN=localhost"
        openssl x509 -req -days 365 -in $CSR_FILE -signkey $KEY_FILE -sha256 -out $CERT_FILE
        openssl x509 -in $CERT_FILE -out $CERT_BUNDLE -outform PEM
    else
        echo "Certifcate Files Found: Skipping Certificate Generation"
fi