# Docker images

## Ex 1 - Build your own image

In order to build your own image locally, you need to create a Dockerfile. Create an empty file `00-docker/Dockerfile` and fill it with the following template:

```dockerfile
FROM python:3.6-alpine 

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

# EX 3: Copy application code (requirements.txt, web.py, templates) here

RUN pip install -r requirements.txt

ENV PORT 80

ENTRYPOINT /usr/local/bin/gunicorn -b :${PORT} --workers 1 --threads 8 web:app
```

After that try to build your application using 

`docker build -t mybidapp .`

Your image should be built successfully. You should find it locally when quering the images `docker images`

## Ex 2 - Start your image locally

Start your image: `docker run mybidapp`. Does the application work?

You should see an error. Tag your image as failed.


## Ex 3 - Update build

Update your Dockerfile so that the application files

- web.py
- requirements.txt
- templates

are copied to the container.

Now you should be able to 


## Bonus - Publish your image to a public registry

Create a user on dockerhub and publish your local image.

Can you use the image of another student?
Try to deploy another version of your image.


## Bonus - Consult dockerfile best practices

Check the Dockerfile best practices:

https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

Could we optimize the build? 
How would you create a docker image of a compiled language?