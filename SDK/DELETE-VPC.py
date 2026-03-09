import openstack

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
)

# -----------------------------
# 2️⃣ Get internal networks only
# -----------------------------
all_networks = list(conn.network.networks())
internal_networks = [n for n in all_networks if not n.is_router_external]

if not internal_networks:
    print("No internal networks found.")
    exit()

print("\nAvailable VPC Networks:")
for i, net in enumerate(internal_networks):
    print(f"{i+1}: {net.name} ({net.id})")

# -----------------------------
# 3️⃣ Select networks to delete
# -----------------------------
while True:
    choice_input = input(
        "Select network numbers to delete (comma separated, e.g. 1,3): "
    ).strip()
    selections = choice_input.split(",")

    try:
        selected_indexes = []
        for sel in selections:
            sel = sel.strip()
            if not sel.isdigit():
                raise ValueError
            index = int(sel)
            if index < 1 or index > len(internal_networks):
                raise ValueError
            selected_indexes.append(index - 1)
        break
    except ValueError:
        print("❌ Invalid input. Please enter valid numbers separated by commas.")

selected_networks = [internal_networks[i] for i in selected_indexes]

print("\n⚠️ You selected the following networks to delete:")
for net in selected_networks:
    print(f"- {net.name} ({net.id})")

confirm = input("Are you sure you want to delete these VPCs and related routers? (yes/no): ").lower()
if confirm != "yes":
    print("Operation cancelled.")
    exit()

# -----------------------------
# 4️⃣ Function to safely delete router
# -----------------------------
def force_delete_router(conn, router):
    print(f"\n🔴 Deleting router: {router.name}")

    # Remove all subnet interfaces
    ports = list(conn.network.ports(device_id=router.id))
    for port in ports:
        if port.device_owner == "network:router_interface":
            try:
                conn.network.remove_interface_from_router(router, port_id=port.id)
                print(f"Removed router interface port {port.id}")
            except Exception as e:
                print(f"Could not remove interface {port.id}: {e}")

    # Remove external gateway
    if router.external_gateway_info:
        try:
            conn.network.update_router(router, external_gateway_info=None)
            print(f"Removed external gateway from router {router.name}")
        except Exception as e:
            print(f"Could not remove external gateway: {e}")

    # Delete router
    try:
        conn.network.delete_router(router.id)
        print(f"🗑️ Router '{router.name}' deleted successfully.")
    except Exception as e:
        print(f"❌ Failed to delete router '{router.name}': {e}")

# -----------------------------
# 5️⃣ Deletion process
# -----------------------------
for network in selected_networks:
    print(f"\n🔹 Deleting network: {network.name} ({network.id})")

    # Get subnets of this network
    subnets = list(conn.network.subnets(network_id=network.id))

    # Find routers attached to subnets
    routers = list(conn.network.routers())
    attached_router_ids = set()
    for subnet in subnets:
        for router in routers:
            for port in conn.network.ports(device_id=router.id):
                for ip in port.fixed_ips:
                    if ip['subnet_id'] == subnet.id:
                        attached_router_ids.add(router.id)
                        break

    # Detach subnets from routers and delete subnets
    for subnet in subnets:
        for router_id in attached_router_ids:
            router = conn.network.get_router(router_id)
            try:
                conn.network.remove_interface_from_router(router, subnet_id=subnet.id)
                print(f"Detached subnet '{subnet.name}' from router '{router.name}'")
            except:
                pass
        try:
            conn.network.delete_subnet(subnet.id)
            print(f"Deleted subnet '{subnet.name}'")
        except Exception as e:
            print(f"Could not delete subnet '{subnet.name}': {e}")

    # Delete the network
    try:
        conn.network.delete_network(network.id)
        print(f"✅ Network '{network.name}' deleted.")
    except Exception as e:
        print(f"Could not delete network '{network.name}': {e}")

    # Force delete attached routers
    for router_id in attached_router_ids:
        router = conn.network.get_router(router_id)
        force_delete_router(conn, router)

# -----------------------------
# 6️⃣ Cleanup leftover ports
# -----------------------------
leftover_ports = [p for p in conn.network.ports() if p.device_owner and p.device_owner != ""]
for port in leftover_ports:
    try:
        conn.network.delete_port(port.id)
        print(f"Deleted leftover port {port.id} ({port.device_owner})")
    except:
        pass  # Ignore ports still in use

print("\n🎉 All selected VPCs, routers, subnets, and leftover ports deleted successfully!")
print("\n🎉 GOOD JOB Captain/ Abdellatif Mohamed Abdeldaim 🎉")
