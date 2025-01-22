import requests
import base64

# Correct URL of the configurations
url = "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt"

print("Fetching configurations from URL...")
response = requests.get(url)
if response.status_code == 200:
    print("Configurations fetched successfully!")
    
    # Remove non-ASCII characters from the response text
    cleaned_content = response.text.encode('ascii', 'ignore').decode('ascii')
    
    # Extract the base64 part (assuming it starts after the first line)
    base64_content = cleaned_content.split("\n", 1)[-1].strip()
    
    # Decode the base64 content
    try:
        decoded_content = base64.b64decode(base64_content).decode('utf-8', errors='ignore')
        print(f"Decoded content length: {len(decoded_content)} characters")
        
        # List of supported protocol prefixes
        protocol_prefixes = [
            "vmess://",
            "vless://",
            "trojan://",
            "ss://",
            "hysteria://",
            "hysteria2://",
            "warp://",
            "wireguard://"
        ]
        
        # Split the decoded content into individual configurations
        configs = []
        for prefix in protocol_prefixes:
            # Split the content by the protocol prefix
            parts = decoded_content.split(prefix)
            if len(parts) > 1:
                # The first part is not a configuration, so skip it
                for part in parts[1:]:
                    # Find the end of the configuration (next protocol prefix or end of string)
                    end_index = len(part)
                    for next_prefix in protocol_prefixes:
                        next_index = part.find(next_prefix)
                        if next_index != -1 and next_index < end_index:
                            end_index = next_index
                    # Extract the configuration
                    config = prefix + part[:end_index]
                    configs.append(config)
        
        print(f"Total configurations found: {len(configs)}")
        
        # Organize configurations by protocol
        protocols = {
            "vmess": [],
            "vless": [],
            "trojan": [],
            "shadowsocks": [],
            "hysteria": [],
            "hysteria2": [],
            "warp": [],
            "wireguard": []
        }
        
        valid_configs_found = False
        for config in configs:
            if not config.strip():  # Skip empty lines
                continue
            if config.startswith("vmess://"):
                protocols["vmess"].append(config)
                valid_configs_found = True
            elif config.startswith("vless://"):
                protocols["vless"].append(config)
                valid_configs_found = True
            elif config.startswith("trojan://"):
                protocols["trojan"].append(config)
                valid_configs_found = True
            elif config.startswith("ss://"):
                protocols["shadowsocks"].append(config)
                valid_configs_found = True
            elif config.startswith("hysteria://"):
                protocols["hysteria"].append(config)
                valid_configs_found = True
            elif config.startswith("hysteria2://"):
                protocols["hysteria2"].append(config)
                valid_configs_found = True
            elif config.startswith("warp://"):
                protocols["warp"].append(config)
                valid_configs_found = True
            elif config.startswith("wireguard://"):
                protocols["wireguard"].append(config)
                valid_configs_found = True
            else:
                print(f"Skipping unknown configuration: {config[:50]}...")  # Print first 50 chars for debugging
        
        if not valid_configs_found:
            print("No valid configurations found.")
            exit(0)  # Exit gracefully if no valid configs are found
        
        # Save each protocol's configurations to a separate file
        for protocol, configs in protocols.items():
            if configs:  # Only create a file if there are configurations
                with open(f"{protocol}.txt", "w", encoding='utf-8') as file:
                    file.write("\n".join(configs))
                print(f"Saved {len(configs)} configurations to {protocol}.txt")
    except Exception as e:
        print(f"Error decoding or processing configurations: {e}")
        exit(1)  # Exit with error if decoding fails
elif response.status_code == 404:
    print("Error: The configurations file was not found (404). Please check the URL.")
    exit(1)
else:
    print(f"Failed to fetch configurations. Status code: {response.status_code}")
    exit(1)
