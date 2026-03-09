# OpenStack Cloud Infrastructure Automation using Terraform

This project demonstrates automated cloud infrastructure provisioning on OpenStack / Huawei Cloud Stack using Terraform and Python SDK automation scripts.

The goal of this project is to automate the deployment and management of cloud infrastructure components such as networking, compute resources, and security configurations.

--------------------------------------------------

PROJECT OVERVIEW

This infrastructure deployment includes:

- VPC Network
- Subnets
- ECS Virtual Machines
- Elastic IP (EIP)
- Security Groups

Infrastructure is deployed using Terraform Infrastructure as Code (IaC) while Python scripts provide additional automation using the OpenStack SDK.

--------------------------------------------------

TECHNOLOGIES USED

- Terraform
- OpenStack CLI
- Python SDK
- Huawei Cloud Stack
- Infrastructure as Code (IaC)

--------------------------------------------------

ARCHITECTURE DIAGRAM


           +-------------------+
           |     Internet      |
           +---------+---------+
                     |
                  Elastic IP
                     |
             +-------+--------+
             |  SecurityGroup |
             +-------+--------+
                     |
                ECS Instance
                     |
                +----+----+
                |  Subnet |
                +----+----+
                     |
                    VPC


--------------------------------------------------

PROJECT STRUCTURE

PS_PROJECT_C

ecs.tf
vpc.tf
eip.tf
SG.tf
providers.tf
output.tf

SDK-Scripts
CREATE-ECS.py
CREATE-VPC.py
CREATE-EIP.py
CREATE-SG.py
DELETE-ECS.py
DELETE-VPC.py
DELETE-EIP.py
DELETE-SG.py

requirements.txt

--------------------------------------------------

INSTALLATION

Clone the repository:

git clone https://github.com/abdelatif2030/cloud-infrastructure-automation-openstack

cd openstack-terraform-cloud

--------------------------------------------------

INSTALL PYTHON DEPENDENCIES

pip install -r requirements.txt

--------------------------------------------------

CONFIGURE OPENSTACK CREDENTIALS

export OS_AUTH_URL=<AUTH_URL>
export OS_USERNAME=<USERNAME>
export OS_PASSWORD=<PASSWORD>
export OS_PROJECT_NAME=<PROJECT>
export OS_USER_DOMAIN_NAME=<DOMAIN>
export OS_PROJECT_DOMAIN_NAME=<DOMAIN>

--------------------------------------------------

DEPLOY INFRASTRUCTURE

Initialize Terraform

terraform init

Check execution plan

terraform plan

Deploy infrastructure

terraform apply

--------------------------------------------------

DESTROY INFRASTRUCTURE

terraform destroy

--------------------------------------------------

PYTHON SDK AUTOMATION

Create ECS instance

python SDK-Scripts/CREATE-ECS.py

Delete ECS instance

python SDK-Scripts/DELETE-ECS.py

--------------------------------------------------

KEY FEATURES

Infrastructure as Code deployment  
OpenStack cloud automation  
Terraform-based provisioning  
Python SDK integration  
Scalable cloud architecture  

--------------------------------------------------

DEVOPS SKILLS DEMONSTRATED

Terraform  
OpenStack  
Infrastructure as Code  
Cloud Networking  
Automation with Python  
Cloud Infrastructure Design

--------------------------------------------------

AUTHOR

DevOps / Cloud Engineer

GitHub Profile  
https://github.com/abdelatif2030

Specializing in

Cloud Infrastructure  
Terraform  
Kubernetes  
Docker  
Automation