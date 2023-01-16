# pull official base image
# FROM python:3.9.6-alpine
FROM python:3.8

# Install dependencies pip
#RUN apt-get update && apt-get install -y \
#    php5-mcrypt \
#    python-pip

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
#RUN apk update \
#    && apk add postgresql-dev gcc python3-dev musl-dev

RUN apt-get -y update \
    && apt-get -y upgrade
#    && apt-get -y install  postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN ["chmod", "+x", "/usr/src/app/docker-entrypoint.sh"]
ENTRYPOINT [ "sh", "/usr/src/app/docker-entrypoint.sh" ]
