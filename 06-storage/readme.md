# Storage

## Redis Storage

Since the data of our auction service is very important, we want to save it to disk. In order to do that we can change our redis configuration to include `appendonly yes`. This way Redis stores every change to a local append only file.

Connect to the redis container and see what is stored in `/data`. Add some bids using the Auction frontend, how does the data in that folder change? 

Now restart the redis instance by deleting the pod

```kubectl delete pods <redis-pod-name>```

Check the data in /data again. Open the Auction Webapp. What's the highest bid?

## Create a Persistent Volume Claim

First we create a volume claim, so that we can mount it to redis afterwards:

```
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: redis-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

Get the information of the created volume:

```kubectl get persistentvolumeclaim```


## Mount the volume 

With our newly created volume, we are able to mount it to store our redis data. We can add this snippet to our redis-deployment:

```yaml
    volumeMounts:
        - name: redis-data-vol
          mountPath: /tmp/
volumes:
    - name: redis-data-vol
      persistentVolumeClaim:
        claimName: redis-data
```

Now delete the redis pod and wait for it to be restarted. What's the highest bid now?

- Can you mount this volume in another pod (web for example)?
- What happens if you scale the redis deployment to multiple instances?
- What do you need to do to mount the volume in multiple pods?