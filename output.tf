#########################################################
# output.tf - Outputs for ECS VM and Floating IP
#########################################################

# Private IP assigned by DHCP to the VM
output "ecs_vm_ip" {
  value       = openstack_compute_instance_v2.ecs_vm.access_ip_v4
  description = "The automatically assigned private DHCP IP of the ECS VM"
}

# Floating IP / EIP (external) if created
output "eip" {
  value       = openstack_networking_floatingip_v2.ecs_eip.address
  description = "The external Floating IP of the ECS VM (if allocated)"
}

# VM Name
output "ecs_vm_name" {
  value       = openstack_compute_instance_v2.ecs_vm.name
  description = "The name of the ECS VM"
}


# VM ID
output "ecs_vm_id" {
  value       = openstack_compute_instance_v2.ecs_vm.id
  description = "The ID of the ECS VM"
}

# Security Group ID
output "ecs_sg_id" {
  value       = openstack_networking_secgroup_v2.ecs_sg_all.id
  description = "ID of the security group applied to the ECS VM"
}


# Subnet ID
output "subnet_id" {
  description = "The ID of the subnet"
  value       = openstack_networking_subnet_v2.subnet.id
}

# Subnet Name
output "subnet_name" {
  description = "The name of the subnet"
  value       = openstack_networking_subnet_v2.subnet.name
}

# Subnet CIDR
output "subnet_cidr" {
  description = "The CIDR block of the subnet"
  value       = openstack_networking_subnet_v2.subnet.cidr
}

# Router ID
output "router_id" {
  description = "The ID of the router"
  value       = openstack_networking_router_v2.router.id
}

# Router Name
output "router_name" {
  description = "The name of the router"
  value       = openstack_networking_router_v2.router.name
}



