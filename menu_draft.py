import os
import subprocess

def execute_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")



def display_namespaces():
    os.system("kubectl get namespaces")

def select_namespace():
    namespace = input("Chọn Namespace: ")
    os.environ["NAMESPACE"] = namespace

def display_pods():
    os.system(f"kubectl get pods -n {os.environ['NAMESPACE']}")

def select_pod():
    pod_name = input("Chọn Pod: ")
    os.environ["POD"] = pod_name

def display_network_policy_menu():
    print("Menu Pod:")
    print("1. Deny_all_traffic_to_an_application.py")
    print("2. Limit_traffic_to_an_application.py")
    print("3. Deny_all_none_whitelisted_traffic_to_a_name_space.py")
    print("4. Deny_all_traffic_from_other_namespaces.py")

def main_menu():
    while True:
        print("Main Menu:")
        print("1. Hiển thị danh sách Namespace và chọn Namespace")
        print("2. Chọn Pod trong Namespace")
        print("3. Thoát")

        choice = input("Chọn tùy chọn: ")

        if choice == "1":
            display_namespaces()
            select_namespace()
        elif choice == "2":
            if "NAMESPACE" not in os.environ:
                print("Bạn cần chọn Namespace trước.")
            else:
                display_pods()
                select_pod()
                display_network_policy_menu()
                pod_choice = input("Chọn tùy chọn cho Pod: ")
                handle_policy_choice(pod_choice)
        elif choice == "3":
            break
        else:
            print("Tùy chọn không hợp lệ.")

def handle_policy_choice(choice):
    if choice == "1":
        execute_script("01_Deny_all_traffic_to_an_application.py")
    elif choice == "2":
        print("Bạn đã chọn Limit_traffic_to_an_application.py cho Pod", os.environ["POD"])
    elif choice == "3":
        print("Bạn đã chọn Deny_all_none_whitelisted_traffic_to_a_name_space.py cho Pod", os.environ["POD"])
    elif choice == "4":
        print("Bạn đã chọn Deny_all_traffic_from_other_namespaces.py cho Pod", os.environ["POD"])
    else:
        print("Tùy chọn không hợp lệ cho Pod.")

if __name__ == "__main__":
    main_menu()
