import yaml
import subprocess
import kubernetes
import json
from kubernetes import client, config

        
config.load_kube_config()

# namespace = selected_namespace
with open("namespace.json", "r") as config_file:
    config = json.load(config_file)
pod_name_2 = config["pod"]
namespace = config["namespace"]

def display_pods(namespace):
    # Lấy danh sách các Pod trong Namespace
    pods = []
    for pod in client.CoreV1Api().list_namespaced_pod(namespace).items:
        pods.append(pod.metadata.name)
    return pods

def select_pod(pods):
    # Hiển thị danh sách Pod và cho phép chọn
    print("Danh sách Pod:")
    for i, pod in enumerate(pods):
        print(f"{i + 1}. {pod}")
    selected = input("Chọn Pod (nhập số tương ứng): ")
    return pods[int(selected) - 1]

network_policy = {
    "apiVersion": "networking.k8s.io/v1",
    "kind": "NetworkPolicy",
    "metadata": {
        "name": "deny-from-" +  "-to-" + pod_name_2 ,
        "namespace": namespace
    },
    "spec": {
        "podSelector": {
            "matchLabels": {
                "app": pod_name_2
            }
        },
        "policyTypes": ["Ingress"],
        "ingress": [
            {
                "from": [
                    {
                        "podSelector": {
                            "matchExpressions": [
                                {"key": "app", "operator": "NotIn", "values": selected_pod}
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
        pods = display_pods(namespace)
        selected_pod = select_pod(pods)
        print("1. Thực thi")
        print("2. Xuất ra file yaml với tên do bạn chọn")
        choice = input("Chọn một lựa chọn (1 hoặc 2): ")

        if choice == "1":
            Limit_traffic_to_an_application_yaml = yaml.dump(network_policy, default_flow_style=False)
            with open("Limit_traffic_to_an_application_yaml", "w") as temp_file:
                temp_file.write(Limit_traffic_to_an_application_yaml)
            apply_kubernetes_yaml('Limit_traffic_to_an_application_yaml')

            break
        elif choice == "2":
            filename = input("Nhập tên file bạn muốn lưu (ví dụ: data.yaml): ")
            with open(filename, 'w') as file:
                yaml.dump(network_policy, file)
            print(f"Đã lưu vào {filename}.yaml!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    select_pod()