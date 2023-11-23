import yaml
import subprocess
import kubernetes
import json
from kubernetes import client, config

config.load_kube_config()

with open("namespace.json", "r") as config_file:
    namespace_config = json.load(config_file)
label_2 = namespace_config.get("label", {}).get("app", "")
namespace = namespace_config["namespace"]


def display_pods(namespace):
    labels = []
    pods = client.CoreV1Api().list_namespaced_pod(namespace).items
    
    for pod in pods:
        pod_labels = pod.metadata.labels
        if pod_labels:
            labels.append(pod_labels)
    
    if not labels:
        print(f"No labels found in the namespace {namespace}")
        return None
    
    return labels

def select_label(labels):   
    if not labels:
        print("No Pod to select.")
        return None

    print("Select the Label you want to deny all traffic to " + label_2 + ": ")
    for i, label in enumerate(labels):
        print(f"{i + 1}. {label}")
    while True:
        selected = input("Select Pod (enter the corresponding number): ")
        try:
            selected_index = int(selected) - 1
            if 0 <= selected_index < len(labels):
                return list(labels)[selected_index]
            else:
                print("Invalid selection. Please re-enter.")
        except ValueError:
            print("Please enter an Integer.")

selected_pod = select_label(display_pods(namespace))

network_policy = {
    "apiVersion": "networking.k8s.io/v1",
    "kind": "NetworkPolicy",
    "metadata": {
        "name": f"deny-from-{selected_pod['app'].lower()}-to-{label_2.lower()}",
        "namespace": namespace
    },
    "spec": {
        "podSelector": {
            "matchLabels": {
                "app": label_2
            }
        },
        "policyTypes": ["Ingress"],
        "ingress": [
            {
                "from": [
                    {
                        "podSelector": {
                            "matchExpressions": [
                                {"key": "app", "operator": "NotIn", "values": [selected_pod['app']]}
                            ]
                        }
                    }
                ]
            }
        ]
    }
}


def apply_kubernetes_yaml(yaml_file_path):
    try:
        # The command you would normally type in the terminal
        cmd = ['kubectl', 'apply', '-f', yaml_file_path]
        
        # Execute the command
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Print the output from the command
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        # If the command failed, it will raise this exception
        print("Error applying YAML:", e.stderr)
    except Exception as e:
        # Catch-all for any other exceptions
        print("An error occurred:", str(e))



while True:
        print("1. Execute")
        print("2. Export to a yaml file with a name of your choice")
        choice = input("Select an option (1 or 2): ")

        if choice == "1":
            # Limit_traffic_to_an_application_yaml = yaml.dump(network_policy, default_flow_style=False)
            # with open("Limit_traffic_to_an_application_yaml", "w") as temp_file:
            #     temp_file.write(Limit_traffic_to_an_application_yaml)
            # apply_kubernetes_yaml('Limit_traffic_to_an_application_yaml')
            yaml_string = yaml.dump(network_policy, default_flow_style=False)
            new_yaml_filename = f"deny-from-{selected_pod['app'].lower()}-to-{label_2.lower()}.yaml"

            with open(new_yaml_filename, "w") as temp_file:
                temp_file.write(yaml_string)

            apply_kubernetes_yaml(new_yaml_filename)

            break
        elif choice == "2":
            filename = input("Enter the file name you want to save (for example, data(.yaml)): ")
            with open(filename, 'w') as file:
                yaml.dump(network_policy, file)
            print(f"Saved to {filename}.yaml!")
            break
        else:
            print("Invalid selection. Please select again.")

