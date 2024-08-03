import subprocess
import getpass

# Define variables
resource_group = "C2175281-key_group"
location = "northeurope"  # Update to the correct location of the existing resource group
public_ip_name = "myPublicIP"
vnet_name = "C2175281-key-vnet"
subnet_name = "default"  # Using the correct subnet name
nic_name = "myNIC2"  # Changed name to avoid conflict
vm_name = "myVM"
username = "azureuser"

# Prompt for password
password = getpass.getpass(prompt="Enter VM admin password: ")

# Check if the resource group exists
def check_resource_group():
    result = subprocess.run([
        "az", "group", "exists",
        "--name", resource_group
    ], capture_output=True, text=True)
    return result.stdout.strip() == 'true'

# Create Resource Group
def create_resource_group():
    if not check_resource_group():
        subprocess.run([
            "az", "group", "create",
            "--name", resource_group,
            "--location", location
        ], check=True)
    else:
        print(f"Resource Group {resource_group} already exists.")

# Create Public IP Address
def create_public_ip():
    subprocess.run([
        "az", "network", "public-ip", "create",
        "--resource-group", resource_group,
        "--name", public_ip_name,
        "--location", location,
        "--allocation-method", "Static",  # Updated to Static
        "--sku", "Standard"  # Added Standard SKU
    ], check=True)

# Create Network Interface
def create_nic():
    subnet_id = subprocess.check_output([
        "az", "network", "vnet", "subnet", "show",
        "--resource-group", resource_group,
        "--vnet-name", vnet_name,
        "--name", subnet_name,
        "--query", "id",
        "--output", "tsv"
    ]).decode().strip()
    
    public_ip_id = subprocess.check_output([
        "az", "network", "public-ip", "show",
        "--resource-group", resource_group,
        "--name", public_ip_name,
        "--query", "id",
        "--output", "tsv"
    ]).decode().strip()
    
    subprocess.run([
        "az", "network", "nic", "create",
        "--resource-group", resource_group,
        "--name", nic_name,
        "--vnet-name", vnet_name,
        "--subnet", subnet_name,
        "--public-ip-address", public_ip_id
    ], check=True)

# Create Virtual Machine
def create_vm():
    nic_id = subprocess.check_output([
        "az", "network", "nic", "show",
        "--resource-group", resource_group,
        "--name", nic_name,
        "--query", "id",
        "--output", "tsv"
    ]).decode().strip()
    
    subprocess.run([
        "az", "vm", "create",
        "--resource-group", resource_group,
        "--name", vm_name,
        "--location", location,
        "--nics", nic_id,
        "--image", "Ubuntu2204",  # Ensuring the image name is valid
        "--size", "Standard_B1s",
        "--admin-username", username,
        "--admin-password", password
    ], check=True)

# Main function
def main():
    print("Checking Resource Group...")
    create_resource_group()
    print("Resource Group checked/created.")
    
    print("Creating Public IP Address...")
    create_public_ip()
    print("Public IP Address created.")
    
    print("Creating Network Interface...")
    create_nic()
    print("Network Interface created.")
    
    print("Creating Virtual Machine...")
    create_vm()
    print("Virtual Machine created.")

if __name__ == "__main__":
    main()

