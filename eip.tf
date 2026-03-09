resource "openstack_networking_floatingip_v2" "ecs_eip" {
  pool        = "EIP-External-Network"  # use the name of your external network
  description = "Floating IP created but not bound to any VM or Port"
}

