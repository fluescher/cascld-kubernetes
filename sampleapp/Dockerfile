FROM python:3.6-alpine 

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

ADD requirements.txt /tmp/app/requirements.txt
RUN pip install -r requirements.txt

ENV PORT 80

ENTRYPOINT /usr/local/bin/gunicorn -b :${PORT} web:app

