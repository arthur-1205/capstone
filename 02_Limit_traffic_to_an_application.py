import yaml

# Nhập giá trị cho app label từ bàn phím
new_app_label = input("Nhập giá trị cho app label: ")

# Tạo đối tượng NetworkPolicy với app label mới
network_policy = {
    "kind": "NetworkPolicy",
    "apiVersion": "networking.k8s.io/v1",
    "metadata": {
        "name": "api-allow"
    },
    "spec": {
        "podSelector": {
            "matchLabels": {
                "app": new_app_label,  # Sử dụng giá trị nhập từ bàn phím
                "role": "api"
            }
        },
        "ingress": [
            {
                "from": [
                    {
                        "podSelector": {
                            "matchLabels": {
                                "app": new_app_label,  # Sử dụng giá trị nhập từ bàn phím
                            }
                        }
                    }
                ]
            }
        ]
    }
}

# Chuyển đối tượng thành YAML và in ra
network_policy_yaml = yaml.dump(network_policy, default_flow_stylAe=False)
with open("network_policy_yaml", "w") as temp_file:
    temp_file.write(network_policy_yaml)
