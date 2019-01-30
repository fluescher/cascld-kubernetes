FROM python:3.6-alpine 

RUN mkdir /tmp/app/
WORKDIR /tmp/app

ADD requirements.txt /tmp/app/requirements.txt
RUN pip install -r requirements.txt

ADD . /tmp/app/

ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", ":8000", "web:app"]

