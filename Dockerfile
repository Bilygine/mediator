FROM python:3.6-stretch
RUN apt-get update \
  && apt-get install ffmpeg gcc sox libsox-fmt-mp3 -y

# set work directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy project
COPY . /usr/src/app/

RUN mkdir -p /usr/src/app/files

EXPOSE 5000

ENTRYPOINT ["flask","run", "-h","0.0.0.0"]
