import yaml

def main():
    # Nhập giá trị cho namespace và podSelector từ bàn phím
    namespace_input = input("Nhập giá trị cho namespace: ")
    pod_selector_input = input("Nhập giá trị cho podSelector (dưới dạng key=value, ví dụ: app=myapp): ")
    key, value = pod_selector_input.split('=')

    # Template cho NetworkPolicy
    network_policy = {
        "kind": "NetworkPolicy",
        "apiVersion": "networking.k8s.io/v1",
        "metadata": {
            "namespace": namespace_input,
            "name": "deny-from-other-namespaces"
        },
        "spec": {
            "podSelector": {
                "matchLabels": {
                    key: value
                }
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

    while True:
        # Menu
        print("1. Thực thi")
        print("2. Xuất ra file yaml với tên do bạn chọn")
        choice = input("Chọn một lựa chọn (1 hoặc 2): ")

        if choice == "1":
            with open('temp.yaml', 'w') as file:
                yaml.dump(network_policy, file)
            print("Đã thực thi!")
            break
        elif choice == "2":
            filename = input("Nhập tên file bạn muốn lưu: ")
            with open(f"{filename}.yaml", 'w') as file:
                yaml.dump(network_policy, file)
            print(f"Đã lưu vào {filename}.yaml!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
            
if __name__ == "__main__":
    main()