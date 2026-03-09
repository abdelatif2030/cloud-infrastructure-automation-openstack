import openstack
import urllib3

# disable SSL warnings
urllib3.disable_warnings()

conn = openstack.connection.Connection(
    auth_url="",
    project_id="",
    username="",
    password="",
    user_domain_name="",
    project_domain_name="",
    region_name="",

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
