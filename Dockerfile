FROM debian:latest
MAINTAINER Nadrieril "nadrieril@eleves.polytechnique.fr"

RUN apt-get -qq update && apt-get install -y python-pip supervisor nginx gunicorn
# RUN pip install gunicorn

ADD requirements.txt /srv/app/requirements.txt
WORKDIR /srv/app
RUN pip install -r requirements.txt

RUN pip install supervisor-stdout

ADD supervisord.conf /etc/supervisord.conf
ADD nginx.conf /etc/nginx/nginx.conf
ADD . /srv/app/

RUN service nginx stop

EXPOSE 8000
CMD supervisord -c /etc/supervisord.conf -n
