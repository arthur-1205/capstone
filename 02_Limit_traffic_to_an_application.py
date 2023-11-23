import yaml
import subprocess
import kubernetes
import json

# Nhập giá trị cho app label từ bàn phím
new_app_label = input("Enter value for App label: ")
# namespace = selected_namespace
with open("namespace.json", "r") as config_file:
    config = json.load(config_file)
namespace = config["namespace"]

# Tạo đối tượng NetworkPolicy với app label mới
network_policy = {
    "kind": "NetworkPolicy",
    "apiVersion": "networking.k8s.io/v1",
    "metadata": {
        "name": "api-allow",
        "namespace": namespace
    },
    "spec": {
        "podSelector": {
            "matchLabels": {
                "app": new_app_label,  
                "role": "api"
            }
        },
        "ingress": [
            {
                "from": [
                    {
                        "podSelector": {
                            "matchLabels": {
                                "app": new_app_label,
                            }
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
            # Menu
        print("1. Execute")
        print("2. Export to a yaml file with a name of your choice")
        choice = input("Select an option (1 or 2): ")

        if choice == "1":
            Limit_traffic_to_an_application_yaml = yaml.dump(network_policy, default_flow_style=False)
            with open("Limit_traffic_to_an_application_yaml", "w") as temp_file:
                temp_file.write(Limit_traffic_to_an_application_yaml)
            apply_kubernetes_yaml('Limit_traffic_to_an_application_yaml')

            break
        elif choice == "2":
            filename = input("Enter the file name you want to save (for example, data(.yaml)): ")
            with open(filename, 'w') as file:
                yaml.dump(network_policy, file)
            print(f"Saved to {filename}.yaml!")
            break
        else:
            print("Invalid selection. Please select again!")
            
