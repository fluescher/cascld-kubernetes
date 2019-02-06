# Security

Connect to a shell in one of the webapplication instances. Check the user the webapplication is running with.

- What user is the webapplication running?
- Why can this be a problem?
- What is the worst thing that could happen?

## Specifying a Security Context

So lets run our webapplication as a non-root user.

Configure the security context of our application and test it:

```yaml
securityContext:
    runAsUser: 1000
```

- What happens to your application? Why?
- What could you do to fix it if you had access to the docker image?
- You can influence the Webapplication port by changeing the environment variable `PORT`

## (Bonus) Redis security context

The base redis image is not under our own control. But we still should be able to run is as non-root. To do this we have the additional issue of file system permissions on our mounted volume. Read https://engineering.bitnami.com/articles/running-non-root-containers-on-openshift.html and try to run Redis without root.

## Isolate Redis 


### Install Cilium 

Not all Kuberenetes NetworkProvider support NetworkPolicies (https://kubernetes.io/docs/tasks/administer-cluster/declare-network-policy/#before-you-begin). To test our network policies we need to install a network provider that supports them. We use [Cilium](https://cilium.io/).

```bash
minikube delete
minikube start --network-plugin=cni --extra-config=kubelet.network-plugin=cni --memory=5120
```

and after minikube started we install Cilium:

```bash
kubectl create -n kube-system -f https://raw.githubusercontent.com/cilium/cilium/1.3.2/examples/kubernetes/addons/etcd/standalone-etcd.yaml
kubectl create -f https://raw.githubusercontent.com/cilium/cilium/v1.3/examples/kubernetes/1.12/cilium.yaml
```

Now wait until all pods are successfully deployed:

```
kubectl get pods -n kube-system
```

After all pods are ready you can redeploy your application. After successful deployment you can enter the bastion pod and bid:

```bash
curl auction # Get currently the highest bid
curl -X POST auction/bid -d bid=1 # Execute a 
```

Unfortunately the minikube ingress controller does not work when cilium is enabled.

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

Now add another NetworkPolicy to prevent the webapplication to connect to anything else than the redis node.

- How would you handle larger configurations?

### Bonus: Limit webapplication egress

To prevent the webapplication to access the internet or other services than redis. We can limit its egress traffic. Create and apply a network policy that prevents the webapp from accessing anything other than redis.
