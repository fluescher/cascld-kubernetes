# 02 - Networking


## 1. Scale your deployment

It's time to scale our deployment. Add another instance of our webapplication:

```bash
kubectl scale --replicas=2 deployment/web
```

Connect to both the instance using port-forwarding.

- What do you notice when comparing the highest bids? 
- Why is that?

## 2. Adding another service

Thankfully our webapplication allows to store state in an external Redis Instance. Let's add our 
redis instance:

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

Watch the application getting deployed. 

## 2. Connect the two services together

Let's use our newly deployed service. Our webapplication can be configured to use it by setting the environment propery `REDIS_HOST` to the IP of our newly deployed Redis instance.

Update the redis deployment descriptor to add the environment property.

- What happens if you access the two webapplication pods?


