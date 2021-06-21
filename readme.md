# CAS Cloud: Container Orchestration

## Setup

### Install kubectl

First, install `kubectl`: https://kubernetes.io/docs/tasks/tools/

### Install minikube

To be able to follow the excercises in this repo you need to have `minikube` installed. 

Follow the steps at https://minikube.sigs.k8s.io/docs/start/ until Step 3.

In the end you should be able to execute `kubectl version`

And see an output similar to this:

```bash
Client Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.1", GitCommit:"5e58841cce77d4bc13713ad2b91fa0d961e69192", GitTreeState:"clean", BuildDate:"2021-05-12T14:18:45Z", GoVersion:"go1.16.4", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"20", GitVersion:"v1.20.2", GitCommit:"faecb196815e248d3ecfb03c680a4507229c2a56", GitTreeState:"clean", BuildDate:"2021-01-13T13:20:00Z", GoVersion:"go1.15.5", Compiler:"gc", Platform:"linux/amd64"}
```