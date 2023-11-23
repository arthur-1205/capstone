import yaml
import subprocess
import kubernetes
import json

# Read namespace and label from the configuration file
with open("namespace.json", "r") as config_file:
    config = json.load(config_file)

namespace = config["namespace"]
selected_label = config["label"]

network_policy = {
    "kind" : "NetworkPolicy",
    "apiVersion":"networking.k8s.io/v1",
    "metadata":{
    "name": f"{selected_label}-deny-all-none-whitelisted"
},
  "namespace": namespace,
  "spec": {
        "podSelector": {},
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

while True:
            # Menu
        print("1. Execute")
        print("2. Export to a yaml file with a name of your choice")
        choice = input("Select an option (1 or 2): ")

        if choice == "1":
            '''Deny_all_none_whitelisted_traffic_to_a_namespace = yaml.dump(network_policy, default_flow_style=False)
            with open("Deny_all_none_whitelisted_traffic_to_a_namespace", "w") as temp_file:
                temp_file.write(Deny_all_none_whitelisted_traffic_to_a_namespace)
            apply_kubernetes_yaml('Deny_all_none_whitelisted_traffic_to_a_namespace')'''
            yaml_string = yaml.dump(network_policy, default_flow_style=False)
            new_yaml_filename = f"Deny-all-none-whitelisted-traffic-to-a-namespace"

            with open(new_yaml_filename, "w") as temp_file:
                temp_file.write(yaml_string)

            apply_kubernetes_yaml(new_yaml_filename)

            break
        elif choice == "2":
            filename = input("Enter the file name you want to save (for example, data(.yaml)) ")
            with open(filename, 'w') as file:
                yaml.dump(network_policy, file)
            print(f"Saved to {filename}.yaml!")
            break
        else:
            print("Invalid selection. Please select again!")
            
