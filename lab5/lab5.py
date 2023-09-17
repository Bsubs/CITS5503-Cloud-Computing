import os
import boto3
import base64
import sys
import argparse
import shutil

# Replace with your student number
student_number = "22489437"
region = "ap-southeast-1"

# Initialize the EC2 client
ec2 = boto3.client('ec2', region)
elb = boto3.client('elbv2', region)

def launch_ec2_instances():
	# Create a security group
	response = ec2.create_security_group(
		GroupName=f"{student_number}-sg",
		Description="security group for development environment"
	)
	security_group_id = response['GroupId']

	# Authorize inbound SSH traffic for the security group
	ec2.authorize_security_group_ingress(
		GroupId=security_group_id,
		IpProtocol="tcp",
		FromPort=22,
		ToPort=22,
		CidrIp="0.0.0.0/0"
	)
	
	# Create a key pair and save the private key to a file
	response = ec2.create_key_pair(KeyName=f"{student_number}-key")
	private_key = response['KeyMaterial']
	private_key_file = f"{student_number}-key.pem"
	
	# Allow writing to the private key file
	os.chmod(private_key_file, 0o666)
	with open(private_key_file, 'w') as key_file:
		key_file.write(private_key)
	# Set the correct permissions for the private key file
	os.chmod(private_key_file, 0o400)
	# Copy the private key file to ~/.ssh directory
	ssh_directory = os.path.expanduser("~/.ssh")
	if not os.path.exists(ssh_directory):
		os.makedirs(ssh_directory)

	shutil.copy(private_key_file, ssh_directory)

	availability_zones = ["ap-southeast-1a", "ap-southeast-1b"]

	for i, az in enumerate(availability_zones):
		instance_name = f"{student_number}-{az}"
		
		instance_params = {
		    'ImageId': 'ami-0df7a207adb9748c7',  
		    'InstanceType': 't2.micro',  
		    'KeyName': f"{student_number}-key",
		    'SecurityGroupIds' : [security_group_id], 
		    'MinCount': 1,
		    'MaxCount': 1,
		    'Placement': {'AvailabilityZone': az},
		    'TagSpecifications': [
		        {
		            'ResourceType': 'instance',
		            'Tags': [{'Key': 'Name', 'Value': instance_name}]
		        }
		    ]
		}

		# Launch an EC2 instance
		response = ec2.run_instances(**instance_params)

		instance_id = response['Instances'][0]['InstanceId']

		# Wait for the instance to be up and running
		ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])

		# Describe the instance to get its public IP address
		response = ec2.describe_instances(InstanceIds=[instance_id])
		public_ip_address = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

		print(f"Instance {i+1} created successfully in Availability Zone {az} with Public IP: {public_ip_address}")


def create_load_balancer():
	vpc_id = 'vpc-02806703abdc316d0'
	security_group_id = 'sg-0021774194b407020'
	subnet_ids = ['subnet-080783bde78702ba9', 'subnet-0da033b36a320696f']
	
	response = elb.create_load_balancer(
		Name='22489437-LoadBalancer',
		Subnets=subnet_ids,
		SecurityGroups=[security_group_id],
		Scheme='internet-facing',  
		Tags=[
		    {
		        'Key': 'Name',
		        'Value': '22489437-LoadBalancer'
		    },
		]
	) 
	
	load_balancer_arn = response['LoadBalancers'][0]['LoadBalancerArn']
	print(f"Load Balancer ARN: {load_balancer_arn}")
	
	# Create a listener for HTTP traffic (Port 80)
	response = elb.create_listener(
		DefaultActions=[
		    {
		        'Type': 'fixed-response',
		        'FixedResponseConfig': {
		            'ContentType': 'text/plain',
		            'StatusCode': '200',
		            'MessageBody': 'OK',
		        },
		    },
		],
		LoadBalancerArn=load_balancer_arn,
		Port=80,
		Protocol='HTTP',
	)

	listener_arn = response['Listeners'][0]['ListenerArn']
	print(f"Listener ARN: {listener_arn}")
	
	# Create a target group
	response = elb.create_target_group(
		Name='22489437-target-group',
		Protocol='HTTP',
		Port=80,
		VpcId=vpc_id,
		TargetType='instance',
	)

	# Get the ARN of the target group
	target_group_arn = response['TargetGroups'][0]['TargetGroupArn']

	# Print the target group ARN
	print(f"Target Group ARN: {target_group_arn}")
	
	instance_1_id = 'i-01624737c61ac9b4d'
	instance_2_id = 'i-0e105acc6d5603f70'

	# Register the instances in the target group
	elb.register_targets(
		TargetGroupArn=target_group_arn,
		Targets=[
		    {'Id': instance_1_id},
		    {'Id': instance_2_id},
		]
	)

	# Print registration status
	print("Targets registered successfully.")

	

def main(argv):
	argParser = argparse.ArgumentParser()
	argParser.add_argument("-i", "--initialise", action='store_true', help="create ec2 instances")
	argParser.add_argument("-lb", "--load-balancer", action='store_true', help="create a load balancer")

	args = argParser.parse_args()
	initialise_flag = args.initialise
	load_balancer_flag = args.load_balancer
	
	if(initialise_flag):
		try:
			launch_ec2_instances()
		except Exception as error:
			print("An error occurred:", error)
	
	if(load_balancer_flag):
		try:
			create_load_balancer()
		except Exception as error:
			print("An error occurred:", error)



if __name__ == "__main__":
	main(sys.argv[1:])
























