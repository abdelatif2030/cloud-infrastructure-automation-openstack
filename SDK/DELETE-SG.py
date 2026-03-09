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
# 2️⃣ Ask for SG names to delete
# -----------------------------
sg_names_input = input("Enter Security Group name(s) to delete (comma separated): ")
sg_names = [name.strip() for name in sg_names_input.split(",") if name.strip()]

if not sg_names:
    print("❌ No names provided. Exiting.")
    exit()

# -----------------------------
# 3️⃣ Delete SGs
# -----------------------------
for sg_name in sg_names:
    # Find matching security groups
    matching_sgs = [sg for sg in conn.network.security_groups() if sg.name == sg_name]
    
    if not matching_sgs:
        print(f"⚠️ No Security Group found with name '{sg_name}'")
        continue

    for i, sg in enumerate(matching_sgs):
        print(f"{i+1}: {sg.name} (ID: {sg.id})")

    # If multiple SGs found, ask which one to delete
    if len(matching_sgs) > 1:
        choice = input(f"Multiple SGs found with name '{sg_name}'. Select number to delete (or 'all'): ").strip().lower()
        if choice == "all":
            selected_sgs = matching_sgs
        elif choice.isdigit() and 1 <= int(choice) <= len(matching_sgs):
            selected_sgs = [matching_sgs[int(choice)-1]]
        else:
            print(f"❌ Invalid choice. Skipping '{sg_name}'.")
            continue
    else:
        selected_sgs = matching_sgs

    # Confirm deletion
    for sg in selected_sgs:
        confirm = input(f"Are you sure you want to delete Security Group '{sg.name}' (ID: {sg.id})? (y/n): ").strip().lower()
        if confirm == "y":
            try:
                conn.network.delete_security_group(sg.id)
                print(f"✅ Security Group '{sg.name}' deleted successfully.")
            except Exception as e:
                print(f"❌ Failed to delete '{sg.name}': {e}")
        else:
            print(f"Skipped Security Group '{sg.name}'")

print("\n🎉 All requested Security Group deletions processed! 🎉")
print("\n🎉 GOOD JOB Captain/ Abdellatif Mohamed Abdeldaim 🎉")
