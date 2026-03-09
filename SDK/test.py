import openstack
import urllib3

# disable SSL warnings
urllib3.disable_warnings()

conn = openstack.connection.Connection(
    auth_url="https://iam-apigateway-proxy.p1xdh.eg/v3",
    project_id="ffbf084c7bd44837a8ca4fcbddb8abb7",
    username="C_test_OMteam_Islam",
    password="Huaweidap12#$",
    user_domain_name="C_test_OMteam",
    project_domain_name="C_test_OMteam",
    region_name="eg-p1xdh",

    # important for HCS
    image_api_version='2',
    verify=False
)

print("\nListing IMS Images...\n")

try:
    for image in conn.image.images():
        print(f"ID: {image.id}")
        print(f"Name: {image.name}")
        print(f"Status: {image.status}")
        print(f"Visibility: {image.visibility}")
        print("-" * 40)

except Exception as e:
    print("Error:", e)