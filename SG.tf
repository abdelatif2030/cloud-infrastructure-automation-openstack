#########################################################
# Security Group - Allow All Ingress & Egress Correct
#########################################################

resource "openstack_networking_secgroup_v2" "ecs_sg_all" {
  name        = "ecs_sg_all"
  description = "Allow all traffic in/out"
}

# Inbound: any protocol, any port
resource "openstack_networking_secgroup_rule_v2" "inbound_all" {
  direction         = "ingress"
  ethertype         = "IPv4"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.ecs_sg_all.id
}

# Outbound: any protocol, any port
resource "openstack_networking_secgroup_rule_v2" "outbound_all" {
  direction         = "egress"
  ethertype         = "IPv4"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.ecs_sg_all.id
}