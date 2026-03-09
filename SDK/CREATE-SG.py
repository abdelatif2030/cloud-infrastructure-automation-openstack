import openstack

# -----------------------------
# 1️⃣ Connect to OpenStack
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
# 2️⃣ Choose Security Group details
# -----------------------------
sg_name = input("Enter Security Group name: ").strip() or "MySecurityGroup"
sg_description = input("Enter Security Group description: ").strip() or "Created via Python SDK"

# -----------------------------
# 3️⃣ Create Security Group
# -----------------------------
security_group = conn.network.create_security_group(
    name=sg_name,
    description=sg_description
)
print(f"\n✅ Security Group '{security_group.name}' created with ID: {security_group.id}\n")

# -----------------------------
# 4️⃣ Function to add a rule
# -----------------------------
def add_rule():
    direction = input("Rule direction (ingress/egress) [ingress]: ").strip().lower() or "ingress"
    protocol = input("Protocol (tcp/udp/icmp/any) [any]: ").strip().lower() or "any"
    port_range = input("Port range (e.g., 22 or 80-100) [any]: ").strip().lower() or "any"
    remote_ip = input("Remote CIDR (e.g., 0.0.0.0/0) [0.0.0.0/0]: ").strip() or "0.0.0.0/0"

    # Handle ports
    if port_range == "any":
        port_min = port_max = None
    elif "-" in port_range:
        try:
            port_min, port_max = map(int, port_range.split("-"))
        except ValueError:
            print("❌ Invalid port range. Skipping rule.")
            return
    else:
        try:
            port_min = port_max = int(port_range)
        except ValueError:
            print("❌ Invalid port. Skipping rule.")
            return

    # Convert protocol "any" to None for OpenStack
    protocol_value = None if protocol == "any" else protocol

    # Create the rule
    try:
        rule = conn.network.create_security_group_rule(
            security_group_id=security_group.id,
            direction=direction,
            protocol=protocol_value,
            port_range_min=port_min,
            port_range_max=port_max,
            remote_ip_prefix=remote_ip
        )
        print(f"✅ Rule added: {direction} {protocol} {port_range} from {remote_ip}")
    except Exception as e:
        print(f"❌ Failed to add rule: {e}")

# -----------------------------
# 5️⃣ Loop to add multiple rules
# -----------------------------
while True:
    add_rule()
    more = input("\nDo you want to add another rule? (y/n): ").strip().lower()
    if more != "y":
        break

print(f"\n🎉 Security Group '{security_group.name}' setup complete! 🎉")
print(f"Security Group ID: {security_group.id}")
print("\n🎉 GOOD JOB Captain/ Abdellatif Mohamed Abdeldaim 🎉")