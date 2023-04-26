from flask import Flask
from kubernetes import client, config
from datetime import datetime,timezone
import os

app = Flask(__name__)

@app.route("/v1/pods/status")
def hello():
    # Load the Kubernetes configuration from within a cluster
    config.load_incluster_config()

    # Create a Kubernetes API client
    v1 = client.CoreV1Api()

    ret = v1.list_namespaced_pod(os.environ.get("X_NAMESPACE"), watch=False)
    pods = ret.items
    pods_names, image_list, restart_count_list, time_list, container_status_list = [], [], [], [], []

# TODO: Needs improvment in the logic
    for pod in pods:
        pods_names.append(pod.metadata.name)
        image_list.append(pod.status.container_statuses[0].image[pod.status.container_statuses[0].image.find(":")+1:])
        restart_count_list.append(pod.status.container_statuses[0].restart_count)
        time_list.append(pod.status.start_time)
        container_status_list.append(pod.status.container_statuses[0].state)

    final_status = []
    message_status= []
    structured_time_list = []
    
    for each_time in time_list:
        each_time = datetime.now(timezone.utc) - each_time
        structured_time_list.append(str(each_time))
            
    for i in container_status_list:
        if i.waiting is None:
            final_status.append("Running")
            message_status.append("NA")
        else:
            final_status.append(i.waiting.reason)
            message_status.append(i.waiting.message)
        
    pods_status = list(zip(pods_names, final_status, restart_count_list, message_status, image_list, structured_time_list))

    list_of_dictionaries = []
    for i in pods_status:
        my_dict = {}
        my_dict['name'] = i[0]
        my_dict['status'] = i[1]
        my_dict['restartCount'] = i[2]
        my_dict['reasonForRestart'] = i[3]
        my_dict['buildImage'] = i[4]
        my_dict['uptime'] = i[5]
        list_of_dictionaries.append(my_dict)
    return (list_of_dictionaries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)





