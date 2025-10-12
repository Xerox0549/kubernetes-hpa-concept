# README.md
# Apache Server on Kubernetes with HPA (Kind Cluster)

This project demonstrates how to deploy an **Apache HTTP Server** on a Kubernetes **kind** cluster and configure **Horizontal Pod Autoscaler (HPA)**.

---

## 📂 Project Structure
```
appache/
 ├── namespace.yml   # Namespace definition
 ├── deployment.yml  # Apache server deployment
 ├── service.yml     # Service to expose Apache
 ├── hpa.yml         # Horizontal Pod Autoscaler
 └── README.md       # Documentation
```

---


## 🚀 Steps to Run

### 1️⃣ Create Project Directory
First, create a project directory and move into it:
```bash
mkdir appache
cd appache
```

---

### 2️⃣ Apply Namespace
The namespace is used to isolate Apache resources. Apply it with:
```bash
kubectl apply -f namespace.yml
```
You can verify with:
```bash
kubectl get ns
```

---

### 3️⃣ Apply Deployment
Deployment manages Apache pods. It ensures the desired number of replicas are always running. Apply with:
```bash
kubectl apply -f deployment.yml
```
Check pods with:
```bash
kubectl get pods -n appache-ns
```

---

### 4️⃣ Apply Service
Service exposes the Apache deployment inside the cluster. Apply with:
```bash
kubectl apply -f service.yml
```
Check service with:
```bash
kubectl get svc -n appache-ns
```

---

### 5️⃣ Port Forward to Access Apache
Since we used `ClusterIP` service type, we need port forwarding to access Apache locally:
```bash
kubectl port-forward svc/appache-service -n appache-ns 8080:80
```
Now open in browser:
```
http://localhost:8080
```

---

### 6️⃣ Apply Horizontal Pod Autoscaler (HPA)
HPA automatically scales the Apache deployment based on CPU usage.
```bash
kubectl apply -f hpa.yml
```
Verify HPA:
```bash
kubectl get hpa -n appache-ns
```

---

### 7️⃣ Verify Resources
- Check pods:
```bash
kubectl get pods -n appache-ns
```
- Check services:
```bash
kubectl get svc -n appache-ns
```
- Check HPA:
```bash
kubectl get hpa -n appache-ns
```

---

## ✅ Expected Output
- Apache server should be accessible at [http://localhost:8080](http://localhost:8080)
- HPA should automatically scale pods based on CPU utilization.

---

##  HPA trafic accelaration 

bash
```
kubectl run -i --tty load-generator --rm --image=busybox /bin/sh
```

- after that we will use @loat_test.py file into the bash script

- And open another terminal for watich the cpu utilization

bash
```
kubectl get hpa -n appache --watch
```
- After 2 minute the script will close automatacally 

- so in between check the 
```
kubectl get pods -n apache 
kubectl get deployment -n apache
```
- And here you can see the cpu utilation is inclease and number of pods are also upgraded

## Role create and use how to make a role and binding 
Bash
```
kubectl auth whoami 

kubectl auth can-i get pods

kubectl apply -f namespace.yml

kubectl auth can-I get pods -n apache
```
- here is the problem if we give access whole access to everyone is risky so we use role for perticuler persion

- as example for a new member can not able to control access of company
Bash 
```
kubectl apply -f deployment.yml 

kubectl auth can-I get deployement -n apache

kubectl auth can-I delete deployment -n apache
```
- there result is unbelievable its say is you can delete but its risky so we use role for particular person

- make a role.yml
bash 
```
kubectl apply -f role.yml
```
- time to check role 
bash 
```
kubectl get role -n apache
```

- but firstly make a service account.yml
bash 
```
vim service-account.yml

kubectl apply -f service-account.yml
```

- now check the service account
bash
```
kubectl get serviceaccount -n apache

kubectl auth can-i get pods -n apache

kubectl auth can-i get pods --as=apache-user -n apache 

kubectl auth can-i get deployment --as=apache-user -n apache 

kubectl auth can-i get service --as=apache-user -n apache 
```

- all have no permissions 

- now here create a roll binding
bash
```
vim role-binding.yml

apply role-binding file

kubectl get rolebinding -n apache
```
- now time to check role configuration
bash
```
kubectl auth can-i get pods --as=apache-user -n apache
```


⚡ Done! You now have **Apache + HPA** running on a **kind cluster**.
