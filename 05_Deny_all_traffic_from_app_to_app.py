import yaml
import subprocess
from kubernetes import client, config

# Tải cấu hình Kubernetes
config.load_kube_config()

# Đọc thông tin về namespace và tên Pod từ tệp JSON
with open("namespace.json", "r") as config_file:
    config_data = yaml.safe_load(config_file)
pod_name_2 = config_data["pod"]
namespace = config_data["namespace"]

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

def apply_kubernetes_yaml(yaml_content):
    try:
        # Sử dụng API Kubernetes để tạo NetworkPolicy
        client.NetworkingV1Api().create_namespaced_network_policy(namespace, yaml_content)
        print("NetworkPolicy đã được tạo thành công.")
    except Exception as e:
        print("Lỗi khi tạo NetworkPolicy:", str(e))

while True:
    pods = display_pods(namespace)
    selected_pod = select_pod(pods)
    print("1. Thực thi")
    print("2. Xuất ra file yaml với tên do bạn chọn")
    choice = input("Chọn một lựa chọn (1 hoặc 2): ")

    if choice == "1":
        network_policy = {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {
                "name": f"deny-from-{selected_pod}-to-{pod_name_2}",
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
                                    "matchLabels": {
                                        "app": selected_pod
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        }
        apply_kubernetes_yaml(network_policy)
        break
    elif choice == "2":
        filename = input("Nhập tên file bạn muốn lưu (ví dụ: data.yaml): ")
        with open(filename, 'w') as file:
            yaml.dump(network_policy, file, default_flow_style=False)
        print(f"Đã lưu vào {filename}!")
        break
    else:
        print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
