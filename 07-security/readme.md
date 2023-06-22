# Security

Connect to a shell in one of the webapplication instances `kubectl exec -it <web-pod-name> sh`. Check the user the webapplication is running with using `whoami`

- What user is the webapplication running?
- Why can this be a problem?
- What is the worst thing that could happen?

## 1. Specifying a Security Context

So lets run our webapplication as a non-root user.

Configure the security context of our application and test it:

```yaml
securityContext:
    runAsUser: 1000
```

- Can you verify our application runs as regular user? Open a shell and execute `whoami` and `ps`

## (Bonus) Isolate Redis 

### Install Cilium 

Not all Kuberenetes NetworkProvider support NetworkPolicies (https://kubernetes.io/docs/tasks/administer-cluster/declare-network-policy/#before-you-begin). To test our network policies we need to install a network provider that supports them. We use [Cilium](https://cilium.io/).

```bash
minikube delete
minikube start --network-plugin=cni --cni=cilium --memory=5120 --driver=<virtualbox|hyperv>
minikube addons enable ingress
```

Now wait until all pods are successfully deployed:

```
kubectl get pods -n kube-system
```

After all pods are ready you can redeploy your application using your `web.yml` and `redis.yml` you created in the previous excercises. After successful deployment you can enter the bastion pod and bid:

```bash
curl auction # Get currently the highest bid
curl -X POST auction -d bid=1 # Place a bid
```

### Add NetworkPolicy

Redis contains our auction data and we don't want this information to be accessible from the whole cluster. But right now exactly that is the case. Try to access the redis instance from our bastion pod:

```bash
nc redis 6379
```

and send the command "INFO". You should receive an list of details of the redis server state.

Now let's try to prevent that:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: redis-network-policy
spec:
  podSelector:
    matchLabels:
      app: redis
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: web
    ports:
    - protocol: TCP
      port: 6379
```

- Can you still access our webapplication from the basion pod.
- How would you handle larger configurations?

### Limit webapplication egress

To prevent the webapplication to access the internet or other services than redis. We can limit its egress traffic. Create and apply a network policy that prevents the webapp from accessing anything other than redis.
