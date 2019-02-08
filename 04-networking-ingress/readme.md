# Networking: Ingress

In all previous excercies we accessed our cluster from within the cluster. To receive traffic from outside, we somehow need to get it in. Kubernetes supports different [ingress controllers](https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers).

We use the Nginx Ingress Controller. It's installation is easy when using minikube. But before we installed it, let's check what happens if we call our minikube node:

Get the IP:

`minikube ip`

and then try to access that ip from your machine:

`curl -i <ip>`

Now lets install our ingress controller:

`minikube addons enable ingress`

This creates new pods. Wait until alle pods are running.

`kubectl get pods --all-namespaces`

Access the node again from your machine:

`curl -i <ip>`

- What changed?
- What was deployed on your cluster? Check all running pods in your cluster: `kubectl get --all-namespaces pods`
- Where does the answer for your HTTP GET come from?

## 1. Create an ingress resource

Let's add a route to our auction backend:

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: auction-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - http:
        paths:
          - path: /
            backend:
              serviceName: auction
              servicePort: 80
```

No if you connect with your browser to the minikube ip you should see the auction app again:

![Webapp](webapp.png "Auction App")

- What happens if you configured a wrong backend?
- Can you access the ingress ressource from outside of the cluster?
- Can you access the ingress ressource from inside the cluster?
