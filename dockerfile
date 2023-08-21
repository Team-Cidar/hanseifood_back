FROM python:3.6
COPY ./ /app/src/
WORKDIR /app/src/
RUN apt-get -y update && apt-get install -y default-libmysqlclient-dev build-essential
RUN apt -y install wget
RUN apt -y install unzip
RUN wget -O /tmp/chrome.deb http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb
RUN apt -y install /tmp/chrome.deb
RUN rm /tmp/chrome.deb
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /app/src/hanseifood/drivers
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh
EXPOSE 8000
ENTRYPOINT ["/bin/bash","./start.sh"]