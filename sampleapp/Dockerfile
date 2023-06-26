FROM python:3.7-alpine 

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

RUN pip install -r requirements.txt

ENV PORT 80

ENTRYPOINT /usr/local/bin/gunicorn -b :${PORT} --workers 1 --threads 8 web:app

