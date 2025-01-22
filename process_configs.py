import requests
import base64

# Correct URL of the configurations
url = "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt"

print("Fetching configurations from URL...")
response = requests.get(url)
if response.status_code == 200:
    print("Configurations fetched successfully!")
    
    # Decode the base64 content
    decoded_content = base64.b64decode(response.text).decode('utf-8')
    print(f"Decoded content length: {len(decoded_content)} characters")
    
    # Split configurations by line
    configs = decoded_content.splitlines()
    print(f"Total configurations found: {len(configs)}")
    
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
        if configs:  # Only create a file if there are configurations
            with open(f"{protocol}.txt", "w") as file:
                file.write("\n".join(configs))
            print(f"Saved {len(configs)} configurations to {protocol}.txt")
        else:
            print(f"No configurations found for {protocol}")
    
    print("Configurations processed and saved successfully!")
elif response.status_code == 404:
    print("Error: The configurations file was not found (404). Please check the URL.")
else:
    print(f"Failed to fetch configurations. Status code: {response.status_code}")
