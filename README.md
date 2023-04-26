## Run app locally/kube-proxy 
### Create a virtual environment, activate it, install the dependencies and run the app.py
```
python3 -m venv venv 
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

## Docker publish
```
docker build -t k8s-pods-status .
docker tag k8s-pods-status REGISTRY/k8s-pods-status:latest
docker push REGISTRY/k8s-pods-status:latest
```

## Run inside k8s 
### Update the namespace value in all the resources of k8s-deployment.yml file
### By default, app will be available as an svc, so ingress routing is required or need to run as a NodePort/LoadBalancer
```
API Details:
- Description - It will fetch the pods status from the namespace it is deployed to.
- Method - Get
- API - /v1/pods/status
```
 
