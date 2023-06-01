# Docker images

## Ex 1 - Pull public image

1. Check the images that are already stored on your machine: `docker images`
2. Pull remote image from registry: `docker pull mysql`
3. Check your local images again. Can you locate your newly downloaded image: `docker images`
4. Remove the downloaded image again: `docker rmi mysql`. Verify that the image is not present anymore.

## Ex 2 - Run public container

Our sample bid app is published on a public container registry as well. 

This means, you can directly start it, without ever building an image or software.

Start the bid app locally: 

`docker run fluescher/cascld`

The application listens on port 80. You can verify this on the log output on the console. Can you access the port? Can you start multiple instances of the bid app at the same time.

You can check your running containers using `docker containers ls`

## Ex 3 - Make application accessible

In order to make the application accessible from your host system using the docker run parameter `-p`. Consult the documentation and expose the application accordingly:

https://docs.docker.com/engine/reference/run/

You should now be able to access the application locally.

## Ex 4 - Limit container resources

Try to limit the memory and cpu of our container. 

First limit the containers memory to the lowest amount possible. Try start with 50MB. How low can you set the limit until the application starts to become unusable?

Secondly try to limit the cpu. Does the application still work if you limit it to 10% of a cpu?

## Bonus - Interact with running containers

If you have the bid app running, you can access a shell inside the container. In order to be able to do that you should start a second terminal or start your container in detached mode. 

You can start an interactive shell inside the container using `docker exec -it <containerid> sh`

can you locate the application sourcecode using the shell inside of the container?

