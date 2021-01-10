FROM python:3.6-alpine
MAINTAINER THS Develper 

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONHTTPSVERIFY 0 

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/community' >> /etc/apk/repositories

RUN apk update && apk add tzdata  \
     && cp -r -f /usr/share/zoneinfo/Asia/Bangkok /etc/localtime

COPY ./requirements.txt .

RUN apk add --no-cache curl jq python3 py3-pip 

RUN apk --update add  python3 py-pip openssl  ca-certificates py-openssl wget  curl 
RUN apk --update add --virtual build-dependencies gcc libffi-dev openssl-dev build-base \
  && apk add --no-cache mariadb-dev \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies 


RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/code
RUN mkdir $APP_HOME
WORKDIR $APP_HOME


ADD ./ /home/app/code

# copy entrypoint_test.sh
COPY ./entrypoint.sh /home/app/code/entrypoint.sh

RUN chmod +x /home/app/code/entrypoint.sh
# run entrypoint.sh

ENTRYPOINT ["sh","/home/app/code/entrypoint.sh"]



