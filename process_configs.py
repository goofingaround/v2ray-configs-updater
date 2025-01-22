import requests
import base64
import os

# URL of the configurations
url = "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_base64_Sub.txt"

# Fetch the configurations
response = requests.get(url)
if response.status_code == 200:
    # Decode the base64 content
    decoded_content = base64.b64decode(response.text).decode('utf-8')
    
    # Split configurations by line
    configs = decoded_content.splitlines()
    
    # Organize configurations by protocol
    protocols = {
        "vmess": [],
        "vless": [],
        "trojan": [],
        "shadowsocks": [],
        "hysteria": [],
        "hysteria2": []
    }
    
    for config in configs:
        if config.startswith("vmess://"):
            protocols["vmess"].append(config)
        elif config.startswith("vless://"):
            protocols["vless"].append(config)
        elif config.startswith("trojan://"):
            protocols["trojan"].append(config)
        elif config.startswith("ss://"):
            protocols["shadowsocks"].append(config)
        elif config.startswith("hysteria://"):
            protocols["hysteria"].append(config)
        elif config.startswith("hysteria2://"):
            protocols["hysteria2"].append(config)
    
    # Save each protocol's configurations to a separate file
    for protocol, configs in protocols.items():
        with open(f"{protocol}.txt", "w") as file:
            file.write("\n".join(configs))
    
    print("Configurations processed and saved successfully!")
else:
    print(f"Failed to fetch configurations. Status code: {response.status_code}")