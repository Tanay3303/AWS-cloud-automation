import boto3
import logging
import json
from datetime import datetime, timedelta, timezone
from botocore.exceptions import ClientError

logging.basicConfig(
    filename='activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# load config

with open ("config.json") as f :
    config = json.load(f)

region = config["region_name"]
instance_type=config ["instance_type"]
image_id= config["image_id"]
bucket_name= config["bucket_name"]
key_name= config["key_name"]

# aws session

aws_m_c = boto3.session.Session(profile_name="default", region_name="eu-north-1")
ec2 = aws_m_c.client("ec2")
s3 = aws_m_c.client("s3")
cloudwatch = aws_m_c.client("cloudwatch")
iam = aws_m_c.client("iam")

logging.info("AWS Session Created Successfully")

# Create s3 bucket

def create_bucket():
    try:
        s3.create_bucket(
        Bucket = bucket_name,
        CreateBucketConfiguration = {"LocationConstraint": region}
        )
        logging.info(f"S3 Bucket Created:{bucket_name}")
        print(f"S3 bucket created: {bucket_name}")

    except ClientError as e :
        logging.error(f"Error creating S3 bucket :{e}")
        print(f"Error creating S3 bucket OR Bucket may already exist :{e}")



# Creating ec2 instance 
def instance ():
    try :
        response = ec2.run_instances(
            ImageId = image_id,
            InstanceType = instance_type,
            KeyName = key_name,
            MinCount = 1,
            MaxCount = 1,
        )

        instance_id = response['Instances'][0]['InstanceId']
        logging.info(f"EC2 instance created : {instance_id}")
        print(f"EC2 instance created : {instance_id}")
        return instance_id
    
    except ClientError as e :
        logging.error(f"EC2 Creation Failed : {e}")
        print(f"EC2 Creation Failed : {e}")

    
# IAM User 

def iam_audit():
    print("\n IAM User Audit : ")
    Iam_users = iam.list_users()['Users']
    for user in Iam_users:
        name = user["UserName"]
        keys = iam.list_access_keys(UserName = name)["AccessKeyMetadata"]
        for k in keys :
            if k ["Status"]=="Active":
                age = (datetime.now(timezone.utc) - k['CreateDate']).days
                if age > 90:
                    logging.warning(f"IAM key age > 90 days for {name}")
                    print(f"User {name} has an active key older than 90 days.")


# Check Security 

def security ():
    try :
        groups = ec2.describe_security_groups()["SecurityGroups"]
        print("\n Security Group result : ")
        for g in groups:
            for permission in g.get("IpPermissions :", []):
                if "FromPort" in permission:
                    if permission["FromPort"] in [22,3389]:
                        logging.warning(f"Open port found in {g['GroupName']}")
                        print(f"Warning : {g["GroupName"]} allows SSH from anywhere!")
    except ClientError as e:
        logging.error(f"Error in Security Check: {e}")
        print(f"Security Error : {e}")

# Monitor CPU 

def cpu (instance_id):
    try:
        metrics= cloudwatch.get_metric_statistics(
            Namespace = "AWS/EC2",
            MetricName= "CPUUtilization",
            Dimensions = [{'Name':"InstanceId", "Value":instance_id}],
            StartTime=datetime.now(timezone.utc) - timedelta(minutes=30),
            EndTime = datetime.now(timezone.utc),
            Period = 300,
            Statistics = ["Average"]
        )
        datapoints  = metrics["Datapoints"]
        if datapoints:
            avg_cpu = datapoints[-1]["Average"]
            print(f"Average CPU Utilization : {avg_cpu:.2f}%")
            if avg_cpu >80:
                logging.warning("High CPU Usage!!")
                print("High CPU Usage!!!")
            else:
                logging.info(f"CPU Usage normal: {avg_cpu:.2f}%")
        else:
            print("No CPU Data.")
    except ClientError as e :
        logging.error(f"Error in CPU: {e}")
        print(f"Error in CPU: {e}")


# Generate Report


def generate_report ():
    report = {
    "region_name": region,
    "instance_type": instance_type,
    "S3_bucket": bucket_name,
    "timestamp": str(datetime.now(timezone.utc)),
    "instanceId": instance_id,
    }
    with open("report.json","w") as f :
        json.dump(report, f, indent=4)
    print("\n Report Generated : report.json")
    logging.info("Report Generated")

# Main 

if __name__ == "__main__":
    print("AWS Cloud Automation amd Monitoring Started\n")
    create_bucket()
    instance_id = instance()
    security ()
    iam_audit()

    if instance_id:
        cpu(instance_id)
    generate_report()
    print("\n All task completed successfully...")