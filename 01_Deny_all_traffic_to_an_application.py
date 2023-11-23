import yaml
import subprocess
import kubernetes
import json
import os

# Read namespace and label from the configuration file
with open("namespace.json", "r") as config_file:
    config = json.load(config_file)

namespace = config["namespace"]
selected_label = config["label"]

# Construct the NetworkPolicy YAML with the label as the pod selector
network_policy = {
    "kind": "NetworkPolicy",
    "apiVersion": "networking.k8s.io/v1",
    "metadata": {
        "name": f"{selected_label}-deny-policy"  # Use the label in the policy name
    },
    "spec": {
        "podSelector": {
            "matchLabels": {
                "app": selected_label  # Use the label in the pod selector
            }
        },
        "policyTypes": ["Ingress"],  # Specify the policy type
        "ingress": []
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

    import os

while True:
    # Menu
    print("1. Execute")
    print("2. Export to a YAML file with a name of your choice")
    choice = input("Select an option (1 or 2): ")

    if choice == "1":
        # Creating a YAML file with a specific name
        yaml_string = yaml.dump(network_policy, default_flow_style=False)
        new_yaml_filename = os.path.join(os.getcwd(), r"deny-all-traffic-from-selectedpod-to-application.yaml")
        with open(new_yaml_filename, "w") as temp_file:
            temp_file.write(yaml_string)

        # Applying the YAML file to Kubernetes
        apply_kubernetes_yaml(new_yaml_filename)
        break

    elif choice == "2":
        # Exporting to a YAML file with a user-specified name
        filename = input("Enter the file name you want to save (for example, data.yaml):")
        with open(filename, 'w') as file:
            yaml.dump(network_policy, file)
        print(f"Saved to {filename}!")

        break

    else:
        print("Invalid selection. Please select again!")
