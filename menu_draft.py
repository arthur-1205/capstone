import kubernetes
from kubernetes import client, config
from kubernetes.config.kube_config import yaml
import os
import subprocess
import json


def execute_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")

def display_namespace():
     #Lấy danh sách các Namespace từ Kubernetes Cluster
    namespaces = []
    for ns in client.CoreV1Api().list_namespace().items:
        namespaces.append(ns.metadata.name)
    return namespaces

def select_namespace(namespaces):
    # Hiển thị danh sách Namespace và cho phép chọn
    print("Danh sách Namespace:")
    for i, ns in enumerate(namespaces):
        print(f"{i + 1}. {ns}")
    selected = input("Chọn Namespace (nhập số tương ứng): ")
    return namespaces[int(selected) - 1]


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

def display_network_policy_menu():
    print("Menu Network Policy:")
    print("1. Deny_all_traffic_to_an_application.")
    print("2. Limit_traffic_to_an_application")
    print("3. Deny_all_none_whitelisted_traffic_to_a_name_space")
    print("4. Deny_all_traffic_from_other_namespace")

def main_menu():
    selected_namespace = ""
    while True:
        print("Main Menu:")
        print("1. Hiển thị danh sách Namespace và chọn Namespace")
        print("2. Chọn Pod trong Namespace")
        print("3. View Network Menu")
        print("4. Thoát")

        choice = input("Chọn tùy chọn: ")
        
        if choice == "1":
            namespaces = display_namespace()
            selected_namespace = select_namespace(namespaces)
            # with open("namespace.json", "w") as config_file:
            #     config = {"namespace": selected_namespace , "pod" : None}
            #     json.dump(config, config_file)
                
        elif choice == "2":
            if selected_namespace is None:
                print("Bạn cần chọn Namespace trước.")
            else:
                pods = display_pods(selected_namespace)
                selected_pods = select_pod(pods)
                with open("namespace.json", "w") as config_file:
                    config = {"namespace": selected_namespace , "pod" : selected_pods}
                    json.dump(config, config_file)
                display_network_policy_menu()
                pod_choice = input("Chọn tùy chọn cho Pod: ")
                handle_policy_choice(pod_choice)
        elif choice == "3":
            main_menu_v2()
        elif choice == "4":
            break
        else:
            print("Tùy chọn không hợp lệ.")


def handle_policy_choice(choice):
    if choice == "1":
        execute_script("01_Deny_all_traffic_to_an_application.py")
    elif choice == "2":
        execute_script("02_Limit_traffic_to_an_application.py")
    elif choice == "3":
        execute_script("03_Deny_all_none_whitelisted_traffic_to_a_name_space.py")
    elif choice == "4":
        execute_script("04_Deny_all_traffic_from_other_namespace.py")
    else:
        print("Tùy chọn không hợp lệ cho Pod.")

def main_menu_v2():
    while True:
        print("\n===== MENU =====")
        print("1. Sử dụng np-viewer")
        print("2. Giải thích về network policies")
        print("3. Thoát")
        choice = input("Nhập lựa chọn của bạn (1/2/3): ")

        if choice == "1":
            use_np_viewer()
        elif choice == "2":
            print("Fetching namespaces...")
            cmd = "kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'"
            namespaces = subprocess.run(cmd.split(), capture_output=True, text=True).stdout.split()
            for i in range(len(namespaces)):
                print(f"{i+1}. {namespaces[i]}")
            #print(namespaces)
            explain_network_policies()
            
        elif choice == "3":
            print("Chương trình kết thúc.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

def use_np_viewer():
    print("Fetching namespaces...")
    cmd = "kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'"
    namespaces = subprocess.run(cmd.split(), capture_output=True, text=True).stdout.split()
    for i in range(len(namespaces)):
        print(f"{i+1}. {namespaces[i]}")
    namespace = input("Nhập namespace (nhấn Enter để hiển thị toàn bộ): ")
    if namespace:
        os.system(f"kubectl np-viewer -n {namespace}")
    else:
        os.system("kubectl np-viewer -A ")

def explain_network_policies():
    namespace = input("Nhập namespace bạn muốn tìm hiểu về network policies: ")
    
    # Lấy danh sách tất cả các network policies trong namespace đó
    cmd = f"kubectl get networkpolicy -n {namespace} -o json"
    result = subprocess.run(cmd.split(), capture_output=True, text=True)
    
    if result.returncode != 0 or "No resources found" in result.stdout:
        print(f"Không có network policies nào trong namespace '{namespace}'.")
        return
    
    policies_data = json.loads(result.stdout).get("items", [])
    
    for policy_data in policies_data:
        policy_name = policy_data.get("metadata", {}).get("name", "")
        print(f"\nChi tiết về network policy '{policy_name}' trong namespace '{namespace}':")
        
        # Giải thích podSelector
        explain_pod_selector(policy_data)
        
        # Giải thích ingress rules
        explain_ingress_rules(policy_data)

def explain_pod_selector(policy_data):
    pod_selector = policy_data.get("spec", {}).get("podSelector", {})
    match_labels = pod_selector.get("matchLabels", {})
    match_expressions = pod_selector.get("matchExpressions", [])
    print(f"- Network policy '{policy_data.get('metadata', {}).get('name', '')}' áp dụng cho:")
    if match_labels:
        print(f"  + Các pods có labels: {match_labels}")
    if match_expressions:
        print("  + Các pods phù hợp với matchExpressions:")
        for expr in match_expressions:
            print(f"    - {expr['key']} {expr['operator']} {expr.get('values', [])}")
    if not match_labels and not match_expressions:
        print("  + Tất cả các pods trong namespace này.")

def explain_ingress_rules(policy_data):
    ingress_rules = policy_data.get("spec", {}).get("ingress", [])
    
    # Nếu không có quy tắc ingress, mặc định sẽ từ chối mọi traffic
    if not ingress_rules:
        print("- Tất cả traffic đến được từ chối mặc định (mặc định là deny-all behavior).")
        return

    print("- Quy tắc ingress cho phép traffic đến từ các nguồn sau:")
    for rule in ingress_rules:
        from_rules = rule.get("from", [])
        
        # Nếu không có 'from' nào được định nghĩa, quy tắc này cho phép tất cả traffic đến
        if not from_rules:
            print("  + Mọi nguồn (mọi địa chỉ IP và pods) - chế độ allow-all.")
        else:
            # Giải thích từng quy tắc 'from'
            for from_rule in from_rules:
                explain_from_rule(from_rule)
        
        # Giải thích các ports được phép
        print_ports(rule.get('ports', []))

def explain_from_rule(from_rule):
    if "ipBlock" in from_rule:
        cidr = from_rule["ipBlock"].get("cidr", "")
        except_ips = from_rule["ipBlock"].get("except", [])
        print(f"  + IPBlock CIDR: {cidr}")
        for ip in except_ips:
            print(f"    - Trừ địa chỉ IP: {ip}")
    
    if "namespaceSelector" in from_rule:
        ns_selector = from_rule['namespaceSelector']
        print_selector("NamespaceSelector", ns_selector)
    
    if "podSelector" in from_rule:
        pod_selector = from_rule['podSelector']
        print_selector("PodSelector", pod_selector)

# Các hàm print_selector và print_ports giữ nguyên


# Các hàm print_selector và print_ports giữ nguyên

    

def print_selector(selector_type, selector):
    match_labels = selector.get("matchLabels", {})
    match_expressions = selector.get("matchExpressions", [])
    
    if match_labels:
        print(f"    - {selector_type} có labels: {match_labels}")
    
    for expr in match_expressions:
        if expr['operator'] == 'In':
            print(f"    - {selector_type} với {expr['key']} trong {expr.get('values', [])}")
        elif expr['operator'] == 'NotIn':
            print(f"    - {selector_type} không chứa {expr['key']} trong {expr.get('values', [])}")
        else:
            print(f"    - {selector_type} với {expr['key']} {expr['operator']} {expr.get('values', [])}")


def print_ports(ports):
    if ports:
        for port in ports:
            protocol = port.get('protocol', 'TCP')
            port_number = port.get('port', 'all')
            print(f"      và qua protocol {protocol} trên port {port_number}")
    else:
        print("      cho mọi ports và protocols")
        
        
config.load_kube_config()

if __name__ == "__main__":
    main_menu()
    
