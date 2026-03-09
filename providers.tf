terraform {
  required_version = ">= 1.3"

  required_providers {
   
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.54.0"
    }

  }
}


provider "openstack" {
  auth_url    = "https://iam-apigateway-proxy.p1xdh.eg/v3"
  region      = "eg-p1xdh"
  user_name   = "C_test_OMteam_Islam"
  password    = "Huaweidap12#$"
  tenant_id   = "ffbf084c7bd44837a8ca4fcbddb8abb7"
  domain_name = "C_test_OMteam"
  endpoint_type = "public"
  insecure    = true
}
