FROM debian:latest
MAINTAINER Nadrieril "nadrieril@eleves.polytechnique.fr"

RUN apt-get -qq update && apt-get install -y python-pip supervisor gunicorn
# RUN pip install gunicorn

ADD requirements.txt /srv/app/requirements.txt
WORKDIR /srv/app
RUN pip install -r requirements.txt

RUN pip install supervisor-stdout
ADD supervisord.conf /etc/supervisord.conf

ADD . /srv/app/
EXPOSE 8000
CMD supervisord -c /etc/supervisord.conf -n
