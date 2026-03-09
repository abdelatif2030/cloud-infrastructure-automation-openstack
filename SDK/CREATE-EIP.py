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
# 2️⃣ Auto-select external network
# -----------------------------
ext_network_name = "EIP-External-Network"
ext_network = next(
    (net for net in conn.network.networks() if net.name == ext_network_name),
    None
)

if not ext_network:
    print(f"❌ External network '{ext_network_name}' not found.")
    exit()

# -----------------------------
# 3️⃣ Create the Floating IP automatically
# -----------------------------
try:
    floating_ip = conn.network.create_ip(
        floating_network_id=ext_network.id,
        description="Auto-created EIP via SDK"
    )
    print(f"\n✅ EIP created successfully!")
    print(f"EIP Address: {floating_ip.floating_ip_address}")
    print(f"EIP ID: {floating_ip.id}")
except Exception as e:
    print(f"❌ Failed to create EIP: {e}")

print("\n🎉 GOOD JOB Captain/ Abdellatif Mohamed Abdeldaim 🎉")