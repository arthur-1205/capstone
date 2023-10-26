def deny_all(namespace, pod_name):
    existing_policies = client.NetworkingV1Api().list_namespaced_network_policy(namespace)
    for existing_policy in existing_policies.items:
        if existing_policy.metadata.name == f"{pod_name}-deny-policy":
            print(f"Network Policy cho Pod {pod_name} đã tồn tại.")
            return 
    policy_deny = {
        "kind": "NetworkPolicy",
        "apiVersion": "networking.k8s.io/v1",
        "metadata": {
            "name": f"{pod_name}-deny-policy"  
        },
        "spec": {
            "podSelector": {
                "matchLabels": {
                    "app": pod_name  
                }
            },
            "ingress": []
        }
    }
    
