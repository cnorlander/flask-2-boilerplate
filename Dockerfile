FROM python:slim
RUN apt-get install -y openssl
VOLUME /deploy
WORKDIR /deploy
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY entrypoint.sh .
RUN ["chmod", "777", "./entrypoint.sh"]
EXPOSE 8080
ENTRYPOINT [ "/bin/bash", "./entrypoint.sh" ] 
