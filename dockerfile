FROM python:3.6
COPY ./ /app/src/
WORKDIR /app/src/
RUN apt-get -y update && apt-get install -y default-libmysqlclient-dev build-essential
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh
EXPOSE 8000
ENTRYPOINT ["/bin/bash","./start.sh"]