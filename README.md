Project Title
Apache Server with Horizontal Pod Autoscaling (HPA) on Kubernetes Kind Cluster

Overview
This project demonstrates how to deploy an Apache web server on a Kubernetes Kind cluster and implement Horizontal Pod Autoscaling (HPA) to automatically scale the number of pods based on CPU utilization. This ensures your application can handle increased traffic efficiently.

Prerequisites
A running Kubernetes Kind cluster.

kubectl installed on your machine.

Getting Started
Step 1: Directory Setup
First, create a new directory for your project files and navigate into it.

Bash

mkdir apache
cd apache
Step 2: Create Kubernetes Manifests
You'll need a few YAML files to define your Kubernetes resources: a namespace, a deployment, a service, and the HPA.

a. Namespace

Create a file named namespace.yml to set up a dedicated namespace for our application.

YAML

# namespace.yml
apiVersion: v1
kind: Namespace
metadata:
  name: apache-server
b. Deployment

Create a file named deployment.yml for the Apache deployment. We'll start with a single replica and define CPU requests and limits, which are essential for HPA to work.

YAML

# deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apache-deployment
  namespace: apache-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: apache
  template:
    metadata:
      labels:
        app: apache
    spec:
      containers:
      - name: apache-container
        image: httpd:2.4
        resources:
          requests:
            cpu: "100m"
          limits:
            cpu: "200m"
        ports:
        - containerPort: 80
c. Service

Create a file named service.yml to expose the Apache deployment. We'll use a NodePort service to make it accessible.

YAML

# service.yml
apiVersion: v1
kind: Service
metadata:
  name: apache-service
  namespace: apache-server
spec:
  selector:
    app: apache
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: NodePort
d. Horizontal Pod Autoscaler (HPA)

Create a file named hpa.yml to set up the HPA. This will automatically scale the number of pods between 1 and 5, targeting a CPU utilization of 50%.

YAML

# hpa.yml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: apache-hpa
  namespace: apache-server
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: apache-deployment
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
Step 3: Apply the Manifests
Use kubectl to apply all the YAML files.

Bash

kubectl apply -f namespace.yml
kubectl apply -f deployment.yml
kubectl apply -f service.yml
kubectl apply -f hpa.yml
Verification and Access
Verify Resources
Check the status of your pods, service, and HPA to ensure everything is running correctly.

Bash

# Check pods
kubectl get pods -n apache-server

# Check service
kubectl get svc -n apache-server

# Check HPA status
kubectl get hpa -n apache-server
Access the Apache Server
To access the Apache server from your local machine, use port forwarding.

Bash

kubectl port-forward svc/apache-service 8080:80 -n apache-server
Now, open your web browser and go to http://localhost:8080 to see the Apache welcome page.