import openstack

# -----------------------------
# 1️⃣ Connect to OpenStack
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
# 2️⃣ Ask user for EIP(s) to delete
# -----------------------------
eip_input = input("Enter EIP address(es) or ID(s) to delete (comma-separated): ")
eip_list = [x.strip() for x in eip_input.split(",") if x.strip()]

if not eip_list:
    print("❌ No EIP entered. Exiting.")
    exit()

# -----------------------------
# 3️⃣ Delete EIPs
# -----------------------------
for eip_ref in eip_list:
    try:
        # Try to find the floating IP by address or ID
        target_ip = None
        # Use conn.network.ips() safely
        if hasattr(conn.network, "ips"):
            floating_ips = conn.network.ips() or []
        else:
            floating_ips = []

        for ip in floating_ips:
            if getattr(ip, "floating_ip_address", None) == eip_ref or getattr(ip, "id", None) == eip_ref:
                target_ip = ip
                break

        if not target_ip:
            print(f"❌ EIP '{eip_ref}' not found.")
            continue

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete EIP {target_ip.floating_ip_address} (ID: {target_ip.id})? (y/n): ").lower()
        if confirm != "y":
            print(f"Skipped EIP {target_ip.floating_ip_address}")
            continue

        # Delete the floating IP
        conn.network.delete_ip(target_ip.id)
        print(f"✅ EIP {target_ip.floating_ip_address} (ID: {target_ip.id}) deleted successfully!")

    except Exception as e:
        print(f"❌ Failed to delete EIP '{eip_ref}': {e}")

print("\n🎉 All requested EIPs processed! 🎉")
print("\n🎉 GOOD JOB Captain/ Abdellatif Mohamed Abdeldaim 🎉")