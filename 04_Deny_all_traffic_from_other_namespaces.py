import yaml
import subprocess
import kubernetes
import json

with open("namespace.json", "r") as config_file:
    config = json.load(config_file)
namespace = config["namespace"]


network_policy = {
        "kind": "NetworkPolicy",
        "apiVersion": "networking.k8s.io/v1",
        "metadata": {
            "namespace": namespace,
            "name": "deny-from-other-namespace-to-namespace-" + namespace
        },
        "spec": {
            "podSelector": {
                "matchLabels": {}
            },
            "ingress": [
                {
                    "from": [
                        {
                            "podSelector": {}
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
            new_yaml_filename = f"deny-all-traffic-from-other-namespaces.yaml"

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
