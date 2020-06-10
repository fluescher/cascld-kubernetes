# 02 - Networking

## 1. Scale your deployment

It's time to scale our deployment. Add another instance of our webapplication:

```bash
kubectl scale --replicas=2 deployment/web
```

This scales the deployment temporarily. Update web.yml as well.

Connect to both the instances using port-forwarding. You need to specify different local ports.

- What do you notice when comparing the highest bids?
- Why is that?

## 2. Adding another service

Thankfully our webapplication allows to store state in an external Redis Instance. Let's add our
redis instance. To do that create a new yaml file called redis.yml with the following content:

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis:alpine
          ports:
            - containerPort: 6379
```

Deploy the application.
Watch the application getting deployed. Have a look at the Redis logfiles.

## 2. Connect the two services together

Let's use our newly deployed service. Our webapplication can be configured to use it by setting the environment propery `REDIS_HOST` to the IP of our newly deployed Redis instance. Have a look at 
https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/ to see how a environment variable can be set.

Update the web deployment descriptor to add the environment property.

- What happens if you access the two webapplication pods?
