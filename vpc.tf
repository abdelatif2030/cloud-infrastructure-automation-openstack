# VPC (Network)
############################

resource "openstack_networking_network_v2" "vpc" {
  name           = "vpc-terraform"
  admin_state_up = true
}

############################
# Subnet
############################

resource "openstack_networking_subnet_v2" "subnet" {
  name            = "subnet-terraform"
  network_id      = openstack_networking_network_v2.vpc.id
  cidr            = "192.168.85.0/24"
  ip_version      = 4
  gateway_ip      = "192.168.85.1"
  enable_dhcp     = true

  dns_nameservers = [
    "10.3.6.8",
    "10.3.6.10"
  ]
}

############################
# Router
############################

resource "openstack_networking_router_v2" "router" {
  name                = "vpc-terraform"
  admin_state_up      = true

}

############################
# Attach Subnet to Router
############################

resource "openstack_networking_router_interface_v2" "router_interface" {
  router_id = openstack_networking_router_v2.router.id
  subnet_id = openstack_networking_subnet_v2.subnet.id
}