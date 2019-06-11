# 03 - Networking: Load Balancing

## 1. Register a service

We already scaled our webapplication. But using the pod IPs does not scale very well. We can register our webapplication pods using a service and exposing them with an DNS entry.

Create a service:

```yml
apiVersion: v1
kind: Service
metadata:
  name: auction
spec:
  selector:
    app: web
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
```

Now access this service from your bastion pod using its name and try to answer the following questions.

- What kind of service did you create?
- Whats the IP of this service?

## 2. Add redis service

Now configure another service for our redis pod and replace the ip of Redis in the web app descriptor.

## 3. Change service types

Now change the type of the created auction service (you need to delete it to change the type: `kubectl delete svc auction`). Compare the output of the name resolution `nslookup auction` from inside your bastion pod.

1. Change the service type to NodePort. What changes? Can you access your service from outside?
2. Add the clusterIP: None to your service definition. What happened now? On which port do you reach the service now?
