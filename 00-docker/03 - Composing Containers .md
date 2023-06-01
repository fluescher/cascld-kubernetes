# Composing containers

Development environments usually need multiple containers composed together. 

## Ex 1 - Use multiple containers together

Our application can persists its state to a database like redis or mysql. 

Start a redis instance in the background: `docker run -d -p 6379:6379 redis:apline`

Can you connect to this instance? `curl telnet://localhost:6379`

Now start our bid app and connect it to redis. You can do this by setting the environment variable `REDIS_HOST=<yourip>`.

Add some bids and restart our app (not redis). Your bid should still be the same.

## Ex 2 - Initialize Docker compose

Docker compose uses a configuration file named `docker-compose.yml`

Create an file in 00-docker and fill it with:

```yml
version: "3"
services:
  redis:
    image: "redis:alpine"
```

Start this configuration using `docker-compose up`

Can you access the redis node?

In order to start our application as well we can add another service to the docker-compose file:

```yml
web:
    build: .
    ports:
      - "8000:80"
    environment:
      - REDIS_HOST=redis
    links:
      - redis
``` 

Stop docker compose `docker-compose down` and restart it `docker-compose up`.

Can you access your service on port 8000?

If you published your image you could reference this as well.

## Bonus - Try mysql as well

Try use the mysql instance of docker-compose. If this works, try to replicate the same behaviour using plain docker.

## Bonus - Replicate docker-compose behaviour using plain docker

You are able to replicate docker-compose by using plain docker commands. 

Try to do that by consuling the documentation: https://docs.docker.com/engine/tutorials/networkingcontainers/

Main commands you need to use are:

- `docker network`
-  docker run parameters: `--net` and `--name`
