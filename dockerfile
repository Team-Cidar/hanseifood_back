FROM python:3.6-slim
COPY ./ /app/src/
WORKDIR /app/src/
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential
RUN pip install -r requirement.txt
RUN django-admin startproject trydjango
CMD ["python", "./hanseifood/manage.py", "runserver", "127.0.0.1:8000"]