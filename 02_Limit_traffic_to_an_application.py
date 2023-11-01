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

# Chuyển đối tượng thành YAML file tạm và in ra
#Limit_traffic_to_an_application_yaml = yaml.dump(network_policy, default_flow_style=False)
#with open("Limit_traffic_to_an_application_yaml", "w") as temp_file:
#    temp_file.write(Limit_traffic_to_an_application_yaml)

#filename = input("Nhập tên file bạn muốn lưu (ví dụ: data.yaml): ")
#with open(filename, 'w') as file:
#    yaml.dump(network_policy, file)
    
while True:
            # Menu
        print("1. Thực thi")
        print("2. Xuất ra file yaml với tên do bạn chọn")
        choice = input("Chọn một lựa chọn (1 hoặc 2): ")

        if choice == "1":
            Limit_traffic_to_an_application_yaml = yaml.dump(network_policy, default_flow_style=False)
            with open("Limit_traffic_to_an_application_yaml", "w") as temp_file:
                temp_file.write(Limit_traffic_to_an_application_yaml)
            break
        elif choice == "2":
            filename = input("Nhập tên file bạn muốn lưu (ví dụ: data.yaml): ")
            with open(filename, 'w') as file:
                yaml.dump(network_policy, file)
            print(f"Đã lưu vào {filename}.yaml!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
            