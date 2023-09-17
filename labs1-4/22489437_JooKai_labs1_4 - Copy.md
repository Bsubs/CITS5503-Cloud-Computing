## Lab 3: Configure S3 Buckets

1. Preparation:
    a. Downloading cloudstorage.py
        <br/><br/>
       ![download](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-13%20152943.png?token=GHSAT0AAAAAACFPD34K6HYINQETWUCCZXV2ZHRP2ZA)
   
   b. Creating rootdir
        <br/><br/>
       ![rootdir](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-13%20153423.png?token=GHSAT0AAAAAACFPD34K7SVQCM3G6XMZK2G2ZHRP25Q)
   
   c. Creating subdir
       <br/><br/>
       ![subdir](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-13%20153612.png?token=GHSAT0AAAAAACFPD34KQ2DAQ7CLF3Z4CY4QZHRP3CA)
   
3. Editing cloudstorage.py to take the initialise argument. The following code segment uses the argparse library to allow the argparse library to take 2 arguments `-i` or `-initialise`. Using either of these 2 arguments will set the `bucketFlag` variable to True. If `bucketFlag` is True, we will attempt to create a bucket in S3. We also catch any exceptions such as `BucketAlreadyExists` and `BucketAlreadyOwnedByYou`. 
   ```
       	argParser = argparse.ArgumentParser()
    	argParser.add_argument("-i", "--initialise", action='store_true', help="create bucket on s3")
    	args = argParser.parse_args()
    	bucketFlag = args.initialise
    	# Insert code to create bucket if not there
    	if(bucketFlag):
    		try:
    			response = s3.create_bucket(Bucket=ROOT_S3_DIR, CreateBucketConfiguration=bucket_config)
    			print("Bucket created successfully:", ROOT_S3_DIR)
    			print(response)
    		except s3.exceptions.BucketAlreadyExists:
    			print("Bucket already exists:", ROOT_S3_DIR)
    		except s3.exceptions.BucketAlreadyOwnedByYou:
    			print("Bucket already owned by you:", ROOT_S3_DIR)
    		except Exception as error:
    			print("An error occurred:", error)
    ```
4. The `upload_file()` method found in `cloudstoraage.py` was modified to add the code required to upload files to S3. The path of the file in S3 is constructed by adding the `ROOT_S3_DIR` which was created in step 2 to the folder path and file name. The file is then uploaded to S3 using the `s3.upload_file()` command.
      ```
          def upload_file(folder_name, file, file_name):
        	# Construct the path for files to be uploaded
        	s3Path = f'{ROOT_S3_DIR}/{folder_name}/{file_name}'
        
        	print("Uploading %s" % file)
        	
        	# Upload the file to S3
        	try:
        		s3.upload_file(file, ROOT_S3_DIR, s3Path)
        		print(f"Uploaded {file_name} to S3")
        	except Exception as e:
        		print(f"Error uploading {file_name}: {e}")
      ```
   <br/><br/>
        ![uploads](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-14%20115517.png?token=GHSAT0AAAAAACFPD34KUYW3GTNXJ5VAGR6MZHRP3HA)
       ![uploads2](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-17%20175214.png?token=GHSAT0AAAAAACFPD34LD7SKC3YG2DLBEB7SZHRP3LA)
       ![uploads3](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-17%20175233.png?token=GHSAT0AAAAAACFPD34K27YQ56C4JWBAB5OSZHRP3PQ)
       ![uploads4](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-17%20175243.png?token=GHSAT0AAAAAACFPD34LONCRLWOCJFYWNTPQZHRP3UQ)
   
6. The following code which is saved in restorefromcloud.py reads the content of the s3 bucket using the command `s3.list_objects` and writes them to the local directory. If the folder structure does not exist in the local directory, the code uses `os.makedirs` to recreate the folder structure from s3 in the local directory.
    ```
        import os
        import boto3
        ROOT_DIR = '.'
        ROOT_S3_DIR = '22489437-cloudstorage'
        REGION = 'ap-southeast-2'
        
        s3 = boto3.client("s3", region_name=REGION)
        bucket_config = {'LocationConstraint': 'ap-southeast-2'}
        
        for key in s3.list_objects(Bucket = ROOT_S3_DIR)['Contents']:
        	if not os.path.exists(os.path.dirname(key['Key'])):
        		os.makedirs(os.path.dirname(key['Key']))
        		
        	print("Downloading %s" % key['Key'])
        	s3.download_file(ROOT_S3_DIR, key['Key'],  key['Key'])
    ```
    <br/><br/>
    ![downloads](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-14%20131746.png?token=GHSAT0AAAAAACFPD34LVAUQVB2JKBH2VS56ZHRP32A)
   
7. Setting up DynamoDB locally
        <br/><br/>
       ![createdir](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-14%20132006.png?token=GHSAT0AAAAAACFPD34KIFRZOBK3MYVWOZKUZHRP36A)
       <br/><br/>
        ![installjre](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-14%20132014.png?token=GHSAT0AAAAAACFPD34KABYP36ZSVKGBHSJEZHRP4DA)
       <br/><br/>
        ![downloaddb](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-14%20132048.png?token=GHSAT0AAAAAACFPD34L6KTFR3BNR752VEEUZHRP4IA)
       <br/><br/>
        ![start](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-14%20132216.png?token=GHSAT0AAAAAACFPD34LQTHESFMHB2DVZDGUZHRP4MQ)
       
8. Creating a table with the following attributes:
        ```
            CloudFiles = {
                    'userId',
                    'fileName',
                    'path',
                    'lastUpdated',
        	    'owner',
                    'permissions'
                    }
                )
        ```
   <br/><br/>
    ![createtable](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-14%20143839.png?token=GHSAT0AAAAAACFPD34KYRNGQUE2R7C2X27AZHRP4RQ)
   
7. The following code which is saved in storeinfo.py is used to get the file information from s3 and put it into the DynamoDB table created in step 6.
       
```
            import boto3

            ROOT_S3_DIR = '22489437-cloudstorage'  
            REGION = 'ap-southeast-2'  
            TABLE = 'CloudFiles'  

            # Connect to S3 and dynamodb
            dynamodb = boto3.resource('dynamodb', region_name=REGION, endpoint_url='http://localhost:8000')  
            table = dynamodb.Table(TABLE)  
            s3 = boto3.client('s3', region_name=REGION)  
            
            # List objects in the specified S3 bucket
            response = s3.list_objects(Bucket=ROOT_S3_DIR)
            
            # Extract relevant information from the S3 response
            userId = str(response['Contents'][0]['Owner']['ID'])
            owner = response['Contents'][0]['Owner']['DisplayName']
            permission = s3.get_bucket_acl(Bucket=ROOT_S3_DIR)['Grants'][0]['Permission']
            
            
            # Iterate through each object in the S3 bucket
            for content in response['Contents']:
                # Get attributes requested by lab sheet 
                item = {
                    'userId': userId,
                    'fileName': content['Key'].split('/')[-1], 
                    'path': content['Key'],
                    'lastUpdated': str(content['LastModified']),
                    'owner': owner,
                    'permissions': permission
                }
                
                print('Putting the following item into DynamoDB table:\n', item, '\n')
                
                # Add the item to the DynamoDB table
                table.put_item(Item=item)
```
<br/><br/>
8. The code is run which stores the details of the two files into the `CloudFiles` table:
<br></br>
![](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-14%20145833.png?token=GHSAT0AAAAAACFPD34KMVW62Z4GXNEUDLMGZHRP4XA)
<br></br>

9. The `CloudFiles` table is scanned using the command `aws dynamodb scan --table-name CloudFiles --endpoint-url http://localhost:8000`. This reveals the details of the two files which were added in step 8.
<br></br>
![](https://raw.githubusercontent.com/Bsubs/CITS5503-Cloud-Computing/main/lab3/Screenshot%202023-08-14%20145934.png?token=GHSAT0AAAAAACFPD34LRNJMJSJ2MQ4JQC6QZHRP43Q)
<br></br>