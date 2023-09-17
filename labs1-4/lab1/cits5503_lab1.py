import boto3

# Get the region data from boto3
ec2 = boto3.client('ec2')
response = ec2.describe_regions()

# Print the header for the columns
print(f"{'Endpoint':<40} {'RegionName'}")

# Print each region's endpoint and region name
for region in response['Regions']:
    print(f"{region['Endpoint']:<40} {region['RegionName']}")


