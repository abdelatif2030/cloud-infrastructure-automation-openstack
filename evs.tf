resource "openstack_blockstorage_volume_v2" "ecs_disk" {
  name = "terraform-evs-disk"
  size = 50    # in GB
  region = "eg-p1xdh"

}

output "ecs_disk_id" {
  description = "The ID of the EVS volume created by Terraform"
  value       = openstack_blockstorage_volume_v2.ecs_disk.id
}

output "ecs_disk_name" {
  description = "The name of the EVS volume"
  value       = openstack_blockstorage_volume_v2.ecs_disk.name
}

output "ecs_disk_size" {
  description = "The size of the EVS volume in GB"
  value       = openstack_blockstorage_volume_v2.ecs_disk.size
}
