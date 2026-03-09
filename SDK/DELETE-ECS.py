import openstack

# -----------------------------
# 1️⃣ Connect to OpenStack (NEW credentials)
# -----------------------------
conn = openstack.connect(
    auth_url="https://iam-apigateway-proxy.p1xdh.eg/v3",
    project_id="ffbf084c7bd44837a8ca4fcbddb8abb7",
    username="C_test_OMteam_Islam",
    password="Huaweidap12#$",
    user_domain_name="C_test_OMteam",
    project_domain_name="C_test_OMteam",
    region_name="eg-p1xdh",
    identity_interface="public",
    verify=False
)

# -----------------------------
# 2️⃣ Ask user for VM names to delete
# -----------------------------
vm_names_input = input("Enter VM name(s) to delete (separate multiple names with commas): ")
vm_names = [name.strip() for name in vm_names_input.split(",")]

# -----------------------------
# 3️⃣ Delete VMs loop
# -----------------------------
for name in vm_names:
    # List all servers with this name
    matching_servers = [s for s in conn.compute.servers() if s.name == name]
    if not matching_servers:
        print(f"No VM found with name '{name}'")
        continue

    # If multiple VMs found, ask which one to delete
    for i, srv in enumerate(matching_servers):
        print(f"{i+1}: {srv.name} (ID: {srv.id})")
    
    if len(matching_servers) > 1:
        choice = int(input(f"Multiple VMs found with name '{name}'. Select number to delete: ")) - 1
        server = matching_servers[choice]
    else:
        server = matching_servers[0]

    # Confirm deletion
    confirm = input(f"Are you sure you want to delete VM '{server.name}' with ID {server.id}? (y/n): ").lower()
    if confirm != "y":
        print(f"Skipped VM '{server.name}'")
        continue

    # Delete VM
    conn.compute.delete_server(server)
    conn.compute.wait_for_delete(server)
    print(f"✅ VM '{server.name}' (ID: {server.id}) deleted successfully")
    print("\n🎉 GOOD JOB Captain/ Abdellatif Mohamed Abdeldaim 🎉")
