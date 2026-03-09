import openstack

# 1️⃣ Connect to OpenStack
conn = openstack.connect(
    auth_url="",
    project_id="",
    username="",
    password="",
    user_domain_name="",
    project_domain_name="",
    region_name="",
    identity_interface="",
    verify=False,
    block_storage_api_version='2'
)

# 2️⃣ Helper function
def choose_option(options, prompt):
    for i, opt in enumerate(options):
        print(f"{i+1}: {opt}")
    choice = int(input(prompt)) - 1
    if choice < 0 or choice >= len(options):
        raise ValueError("Invalid choice")
    return choice

# 3️⃣ Number of VMs
num_vms = int(input("Enter number of VMs to create: "))

# 4️⃣ Predefined flavors, images, disk types
flavors_list = [
    "Com_1vCPU_2vRam", "Com_2vCPU_4vRam", "Com_4vCPU_8vRam",
    "Com_4vCPU_16vRam", "Com_4vCPU_32vRam", "Com_4vCPU_64vRam",
    "Com_8vCPU_16vRam", "Com_8vCPU_32vRam", "Com_16vCPU_32vRam",
    "Com_16vCPU_64vRam", "Com_32vCPU_128vRam", "Com_64vCPU_64vRam"
]

images_list = ["image-PublicImage-Centos79", "Ubuntu-OpenstackCLI"]
disk_types_list = ["SSD1", "SSD"]

# 5️⃣ Select network
networks = list(conn.network.networks())
network_names = [net.name for net in networks]
network_choice = choose_option(network_names, "Select network number: ")
network_id = networks[network_choice].id

# 6️⃣ Select security group
sec_groups = list(conn.network.security_groups())
allowed_sec_groups = [sg.name for sg in sec_groups if sg.name in ["default", "ecs_sg_allow_all"]]
sec_group_choice = choose_option(allowed_sec_groups, "Select security group number: ")
selected_sec_group = allowed_sec_groups[sec_group_choice]

# 7️⃣ External network ID for Floating IPs
external_network_id = "b027e61b-e8ca-4ceb-8cc6-a65ae1c161af"

# 8️⃣ Create VMs loop
for vm_index in range(num_vms):
    print(f"\n=== Configuring VM #{vm_index + 1} ===")
    vm_name = input("Enter VM name: ")

    # Flavor lookup
    flavor_choice = choose_option(flavors_list, "Select flavor number: ")
    flavor_name = flavors_list[flavor_choice]
    flavor_obj = next((f for f in conn.compute.flavors() if f.name == flavor_name), None)
    if not flavor_obj:
        raise ValueError(f"Flavor '{flavor_name}' not found")
    flavor_id = flavor_obj.id

    # Image lookup
    image_choice = choose_option(images_list, "Select image number: ")
    image_name = images_list[image_choice]
    image_obj = next((img for img in conn.compute.images() if img.name == image_name), None)
    if not image_obj:
        raise ValueError(f"Image '{image_name}' not found")
    image_id = image_obj.id

    # Metadata
    owner = input("Enter owner name (optional): ")
    metadata = {"owner": owner} if owner else {}

    # Data disks
    block_devices = []
    num_disks = int(input("Enter number of data disks for this VM: "))
    for disk_index in range(num_disks):
        print(f"\nConfiguring Disk #{disk_index + 1}")
        disk_size = int(input("Enter disk size in GB: "))
        disk_choice = choose_option(disk_types_list, "Select disk type: ")
        disk_type = disk_types_list[disk_choice]

        volume = conn.block_storage.create_volume(
            size=disk_size,
            volume_type=disk_type,
            name=f"{vm_name}_disk{disk_index+1}"
        )
        volume = conn.block_storage.wait_for_status(volume, status="available")
        block_devices.append({
            "uuid": volume.id,
            "source_type": "volume",
            "destination_type": "volume",
            "boot_index": None,  # None for additional data disks
            "delete_on_termination": True
        })

    # Create VM
    server = conn.compute.create_server(
        name=vm_name,
        image_id=image_id,
        flavor_id=flavor_id,
        networks=[{"uuid": network_id}],
        metadata=metadata,
        security_groups=[{"name": selected_sec_group}],
        block_device_mapping_v2=block_devices if block_devices else None
    )
    server = conn.compute.wait_for_server(server)
    print(f"\n✅ VM '{server.name}' created successfully with ID: {server.id}")

    # 9️⃣ Optional: Attach Floating IP
    attach_fip = input("Do you want to allocate and attach an Elastic IP to this VM? (y/n): ").lower()
    if attach_fip == "y":
        fip = conn.network.create_ip(floating_network_id=external_network_id)
        conn.compute.add_floating_ip_to_server(server, fip.floating_ip_address)
        print(f"✅ Floating IP {fip.floating_ip_address} attached to VM '{server.name}'")

print("\n🎉 All VMs created successfully! 🎉")