resource "openstack_compute_instance_v2" "ecs_vm" {
  name              = "ecs_abdellatif-test-tf"
  image_name        = "Ubuntu-OpenstackCLI"
  flavor_name       = "Com_2vCPU_4vRam"
  availability_zone = "az0.dc0"

  network {
    uuid = "876f280f-f9c1-460f-b12f-28daf393820a"
  }

  security_groups = ["default"]

  metadata = {
    project = "0f86a840a41e455c9b72eefc13055573"
    owner   = "G_test_OMteam"
  }

  lifecycle {
    create_before_destroy = true
  }
}