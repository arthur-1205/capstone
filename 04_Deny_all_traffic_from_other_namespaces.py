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
            "name": "deny-from-other-namespace to namespace: " + namespace
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
            # Menu
        print("1. Thực thi")
        print("2. Xuất ra file yaml với tên do bạn chọn")
        choice = input("Chọn một lựa chọn (1 hoặc 2): ")

        if choice == "1":
            Deny_all_traffic_from_other_namespaces = yaml.dump(network_policy, default_flow_style=False)
            with open("Deny_all_traffic_from_other_namespaces", "w") as temp_file:
                temp_file.write(Deny_all_traffic_from_other_namespaces)
            apply_kubernetes_yaml('Deny_all_traffic_from_other_namespaces')

            break
        elif choice == "2":
            filename = input("Nhập tên file bạn muốn lưu (ví dụ: data.yaml): ")
            with open(filename, 'w') as file:
                yaml.dump(network_policy, file)
            print(f"Đã lưu vào {filename}.yaml!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
            
