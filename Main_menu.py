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
    print("List of Namespaces:")
    for i, ns in enumerate(namespaces):
        print(f"{i + 1}. {ns}")
    selected = input("Select Namespace (enter the corresponding number): ")
    return namespaces[int(selected) - 1]


def display_pods(namespace):
    labels = []
    pods = client.CoreV1Api().list_namespaced_pod(namespace).items
    
    for pod in pods:
        pod_labels = pod.metadata.labels
        if pod_labels:
            labels.append(pod_labels)
    
    if not labels:
        print(f"No labels found in the namespace {namespace}")
        return None
    
    return labels

def select_label(labels):   
    if not labels:
        print("No Pod to select.")
        return None

    print("List of Labels:")
    for i, label in enumerate(labels):
        print(f"{i + 1}. {label}")

    while True:
        selected = input("Select Pod (enter the corresponding number): ")
        try:
            selected_index = int(selected) - 1
            if 0 <= selected_index < len(labels):
                return list(labels)[selected_index]
            else:
                print("Invalid number. Please re-enter!")
        except ValueError:
            print("Please enter an Integer!!")


def display_network_policy_menu():
    print("Menu Network Policy:")
    print("01. Deny_all_traffic_to_an_application")
    print("02. Limit_traffic_to_an_application")
    print("03. Deny_all_none_whitelisted_traffic_to_a_name_space")
    print("04. Deny_all_traffic_from_other_namespace")
    print("05. Deny_all_traffic_from_app_to_app")

def main_menu():
    selected_namespace = ""
    while True:
        print("\n===== Main MENU =====")
        print("1. View Network Menu")
        print("2. Display the Namespace list and select Namespace")
        print("3. Select Pod in Namespace")
        print("4. Exit \n")

        choice = input("Select options: ")
        if choice == "1":
            main_menu_v2()
            
        elif choice == "2":
            namespaces = display_namespace()
            selected_namespace = select_namespace(namespaces)
            # with open("namespace.json", "w") as config_file:
            #     config = {"namespace": selected_namespace , "pod" : None}
            #     json.dump(config, config_file)
                
        elif choice == "3":
            if selected_namespace == "":
                print("You need to choose Namespace first!")
            else:
                labels = display_pods(selected_namespace)
                selected_label = select_label(labels)
                with open("namespace.json", "w") as config_file:
                    config = {"namespace": selected_namespace, "label": selected_label}
                    json.dump(config, config_file)
                display_network_policy_menu()
                pod_choice = input("Select Policy for: ")
                handle_policy_choice(pod_choice)
       
        elif choice == "4":
            print("Thanks for using this Tools!!")
            break
        else:
            print("Invalid option.")


def handle_policy_choice(choice):
    if choice == "1":
        execute_script("01_Deny_all_traffic_to_an_application.py")
    elif choice == "2":
        execute_script("02_Limit_traffic_to_an_application.py")
    elif choice == "3":
        execute_script("03_Deny_all_none_whitelisted_traffic_to_a_name_space.py")
    elif choice == "4":
        execute_script("04_Deny_all_traffic_from_other_namespaces.py")
    elif choice == "5":
        execute_script("05_Deny_all_traffic_from_app_to_app.py")    
    else:
        print("Invalid option for Pod.")

def main_menu_v2():
    while True:
        print("\n===== MENU =====")
        print("1. Use np-viewer and explain Network Policies")
        print("2. Exit")
        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            use_np_viewer_and_explain()  
        elif choice == "2":
            print("The program Ends.")
            break
        else:
            print("Invalid selection. Please try again!")

def use_np_viewer_and_explain():
    print("Fetching namespaces...")
    cmd = ["kubectl", "get", "namespaces", "-o", "jsonpath={.items[*].metadata.name}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error fetching namespaces")
        return
    
    namespaces = result.stdout.split()
    for i, namespace in enumerate(namespaces):
        print(f"{i+1}. {namespace}")
    
    namespace_index = input("Select namespace by Number (press Enter to display all): ")

    if namespace_index.isdigit() and 0 < int(namespace_index) <= len(namespaces):
        selected_namespace = namespaces[int(namespace_index) - 1]
        # Using the list form of subprocess.run to avoid shell interpretation issues
        subprocess.run(["kubectl", "np-viewer", "-n", selected_namespace])
        explain_network_policies(selected_namespace)
    else:
        subprocess.run(["kubectl", "np-viewer", "-A"])
        for ns in namespaces:
            explain_network_policies(ns)

def explain_network_policies(namespace):
    
    
    # Lấy danh sách tất cả các network policies trong namespace đó
    cmd = f"kubectl get networkpolicy -n {namespace} -o json"
    result = subprocess.run(cmd.split(), capture_output=True, text=True)
    
    if result.returncode != 0 or "No resources found" in result.stdout:
        print(f"There are no network policies in the namespace '{namespace}'.")
        return
    
    policies_data = json.loads(result.stdout).get("items", [])
    
    for policy_data in policies_data:
        policy_name = policy_data.get("metadata", {}).get("name", "")
        print(f"\nDetails about network policy '{policy_name}' in namespace '{namespace}':")
        
        # Giải thích podSelector
        explain_pod_selector(policy_data)
        
        # Giải thích ingress rules
        explain_ingress_rules(policy_data)

def explain_pod_selector(policy_data):
    pod_selector = policy_data.get("spec", {}).get("podSelector", {})
    match_labels = pod_selector.get("matchLabels", {})
    match_expressions = pod_selector.get("matchExpressions", [])
    print(f"- Network policy '{policy_data.get('metadata', {}).get('name', '')}' apply for:")
    if match_labels:
        print(f"  + Pods have labels: {match_labels}")
    if match_expressions:
        print("  + Pods that match matchExpressions:")
        for expr in match_expressions:
            print(f"    - {expr['key']} {expr['operator']} {expr.get('values', [])}")
    if not match_labels and not match_expressions:
        print("  + All pods in this namespace.")

def explain_ingress_rules(policy_data):
    ingress_rules = policy_data.get("spec", {}).get("ingress", [])
    
    # Nếu không có quy tắc ingress, mặc định sẽ từ chối mọi traffic
    if not ingress_rules:
        print("- All incoming traffic is denied by default (default is deny-all behavior).")
        return

    print("- The ingress rule allows traffic from the following sources:")
    for rule in ingress_rules:
        from_rules = rule.get("from", [])
        
        # Nếu không có 'from' nào được định nghĩa, quy tắc này cho phép tất cả traffic đến
        if not from_rules:
            print("  + All sources (all IP addresses and pods) - allow-all mode.")
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

def print_selector(selector_type, selector):
    match_labels = selector.get("matchLabels", {})
    match_expressions = selector.get("matchExpressions", [])
    
    if match_labels:
        print(f"    - {selector_type} have labels: {match_labels}")
    
    for expr in match_expressions:
        if expr['operator'] == 'In':
            print(f"    - {selector_type} with {expr['key']} trong {expr.get('values', [])}")
        elif expr['operator'] == 'NotIn':
            print(f"    - {selector_type} does not contain {expr['key']} trong {expr.get('values', [])}")
        else:
            print(f"    - {selector_type} with {expr['key']} {expr['operator']} {expr.get('values', [])}")


def print_ports(ports):
    if ports:
        for port in ports:
            protocol = port.get('protocol', 'TCP')
            port_number = port.get('port', 'all')
            print(f"      and via protocol {protocol} on port {port_number}")
    else:
        print("      for all ports and protocols")
        
        
config.load_kube_config()

if __name__ == "__main__":
    main_menu()
    
