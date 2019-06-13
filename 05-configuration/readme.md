# Configuration

Have a look at the output of the redis instance:

`kubectl logs <redis-pod-name>`

Do you see a line like:

```
1:C 05 Feb 2019 07:26:23.659 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
```

## 1. Add a ConfigMap

So let's give Redis a configuration file. Create a ConfigMap with the following content:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
data:
  redis.config: |
    tcp-backlog 128
```

Add the following snippets to the redis container specification:

```yaml
command: ["redis-server"]
args: ["/tmp/redis.config"]
volumeMounts:
  - name: redis-config-vol
    mountPath: /tmp/
```

and this:

```yaml
volumes:
  - name: redis-config-vol
    configMap:
      name: redis-config
```

Have a look at the kubernetes documentation to see a working example: https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#add-configmap-data-to-a-specific-path-in-the-volume

After you applied your changes you can have another look at the logs of the redis instance. There shouldn't be any more warnings.

## 2. Check our changes

To check what we changed inside the container let's connect to the redis pod:

`kubectl exec -it <redis-pod-name> -- /bin/sh`

- What is stored in the /tmp folder?
- What is the content of the config file?
- What happens if you change the ConfigMap?
