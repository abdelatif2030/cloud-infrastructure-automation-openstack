import openstack
import ipaddress

# -----------------------------
# 1️⃣ Connect to OpenStack (NEW credentials)
# -----------------------------
conn = openstack.connect(
    auth_url="",
    project_id="",
    username="",
    password="",
    user_domain_name="",
    project_domain_name="",
    region_name="",
    identity_interface="",
    verify=False

# -----------------------------
# 2️⃣ Helper function
# -----------------------------
def choose_option(options, prompt):
    for i, opt in enumerate(options):
        print(f"{i+1}: {opt}")
    choice = input(prompt).strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
        raise ValueError("Invalid choice")
    return int(choice) - 1

# -----------------------------
# 3️⃣ Input VPC/Network details
# -----------------------------
vpc_name = input("Enter VPC (network) name: ").strip()
subnet_name = input("Enter subnet name: ").strip()

# CIDR validation
while True:
    cidr_input = input("Enter subnet CIDR (e.g., 192.168.85.0/24): ").strip()
    try:
        network_cidr = ipaddress.IPv4Network(cidr_input)
        break
    except ValueError:
        print("Invalid CIDR, try again.")

# Gateway IP
gateway_ip = input("Enter gateway IP (leave empty for auto): ").strip()
if not gateway_ip:
    gateway_ip = str(list(network_cidr.hosts())[0])
    print(f"Using auto-assigned gateway IP: {gateway_ip}")

# DNS nameservers
dns_input = input("Enter DNS nameservers separated by commas (leave empty for default): ").strip()
dns_nameservers = [x.strip() for x in dns_input.split(",")] if dns_input else None

# -----------------------------
# 4️⃣ Create Network (VPC)
# -----------------------------
network = conn.network.create_network(
    name=vpc_name,
    admin_state_up=True
)
print(f"✅ Network '{network.name}' created with ID: {network.id}")

# -----------------------------
# 5️⃣ Create Subnet
# -----------------------------
subnet = conn.network.create_subnet(
    name=subnet_name,
    network_id=network.id,
    ip_version=4,
    cidr=str(network_cidr),
    gateway_ip=gateway_ip,
    enable_dhcp=True,
    dns_nameservers=dns_nameservers
)
print(f"✅ Subnet '{subnet.name}' created with ID: {subnet.id}")

# -----------------------------
# 6️⃣ Router creation / attach
# -----------------------------
attach_router = input("Do you want to attach this subnet to a router for internet access? (y/n): ").lower()
if attach_router == 'y':
    routers = list(conn.network.routers())

    # Build options list: existing routers + "Create new router"
    router_options = [r.name for r in routers] + ["Create new router"]
    router_choice = choose_option(router_options, "Select router number: ")

    if router_choice == len(router_options) - 1:
        # User chose to create a new router
        router_name = input("Enter a name for the new router: ").strip()

        # Select external network
        ext_networks = [
            n for n in conn.network.networks()
            if n.is_router_external or "external" in n.name.lower() or "eip" in n.name.lower()
        ]
        if not ext_networks:
            raise Exception("No external network found to attach router!")

        print("Select external network for router (internet):")
        ext_choice = choose_option([n.name for n in ext_networks], "Enter external network number: ")
        ext_network = ext_networks[ext_choice]

        router = conn.network.create_router(
            name=router_name,
            admin_state_up=True,
            external_gateway_info={"network_id": ext_network.id}
        )
        print(f"✅ Router '{router.name}' created with ID: {router.id}")

    else:
        # User selected an existing router
        router = routers[router_choice]
        print(f"✅ Using existing router: {router.name}")

    # Attach subnet to router
    conn.network.add_interface_to_router(router, subnet_id=subnet.id)
    print(f"✅ Subnet '{subnet.name}' attached to router '{router.name}'")
    print("\n🎉 GOOD JOB Captain/ Abdellatif Mohamed Abdeldaim 🎉")