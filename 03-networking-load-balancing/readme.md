# 03 - Networking: Load Balancing


## 1. Register a service

We already scaled our webapplication. But using the pod IPs does not scale very well. We can register our webapplciation pods using a service and exposing them with an DNS entry.

Create a service:

```yml
apiVersion: apps/v1
kind: Service
metadata:
  name: auction
spec:
  selector:
    app: web
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

Now access this service using its name and try to answer the following questions.

- What kind of service did you create?
- Whats the IP of this service?
- Which instance do you connect to? Maybe turn of redis and try again. What do you see?

## 2. Add different Service type

Now change the type of the created service (you need to delete it to change the type: `kubectl delete svc auction`). Compare the output of the name resolution `nslookup auction`

1. Change the service type to NodePort. What changes? Can you access your service from outside?
2. Add the clusterIP: None to your service definition. What happened now? On which port do you reach the service now?

## 3. Add redis service

Now configure another service for our redis pod and replace the ip of the redis port in the web app descriptor.