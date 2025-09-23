# HPA Load Test Script for Local Kubernetes (Kind/Minikube)
# Duration: ~2 minutes

import subprocess
import time

# Variables
duration_seconds = 120  # 2 minutes
service_url = 'http://localhost:8080'  # Change if different port

# Start the load generator
print(f"Starting load test on {service_url} for {duration_seconds} seconds...")
start_time = time.time()

try:
    while time.time() - start_time < duration_seconds:
        # Use wget to hit the service
        subprocess.run(['wget', '-q', '-O-', service_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except KeyboardInterrupt:
    print("Load test interrupted")

print("Load test finished. Check HPA status with:")
print("kubectl get hpa -n appache-ns --watch")
