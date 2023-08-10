FROM python:3.6
COPY ./ /app/src/
WORKDIR /app/src/
RUN apt-get -y update && apt-get install -y default-libmysqlclient-dev build-essential
RUN apt -y install wget
RUN apt -y install unzip
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt -y install ./google-chrome-stable_current_amd64.deb
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /app/src/hanseifood/drivers
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh
EXPOSE 8000
ENTRYPOINT ["/bin/bash","./start.sh"]