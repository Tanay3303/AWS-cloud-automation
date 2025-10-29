# from datetime import datetime, timedelta, timezone
# import boto3

# aws_m_c = boto3.session.Session(profile_name="default", region_name="eu-north-1")
# ec2 = aws_m_c.client("ec2")

# def list_running_instances():
#     try:
#         # Describe all instances
#         response = ec2.describe_instances()
#         print("\n Running EC2 Instances:\n")

#         for reservation in response['Reservations']:
#             for instance in reservation['Instances']:
#                 state = instance['State']['Name']

#                 # Only show running instances
#                 if state == 'running':
#                     instance_id = instance['InstanceId']
#                     launch_time = instance['LaunchTime']  # UTC time
#                     name = "No Name"


#                     # Calculate uptime
#                     now = datetime.now(timezone.utc)
#                     uptime = now - launch_time
#                     hours, remainder = divmod(uptime.total_seconds(), 3600)
#                     minutes, _ = divmod(remainder, 60)

#                     print(f"Instance Name : {name}")
#                     print(f"Instance ID   : {instance_id}")
#                     print(f"Launch Time   : {launch_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
#                     print(f"Uptime        : {int(hours)} hours {int(minutes)} minutes\n")

#     except Exception as e:
#         print(f"Error listing instances: {e}")


# list_running_instances()


import boto3

# Initialize EC2 client (make sure region matches your AWS Console)
aws_m_c = boto3.session.Session(profile_name="default", region_name="ap-south-1")
ec2 = aws_m_c.client("ec2")

def list_instance_ids():
    try:
        # Fetch instances of all 3 states
        response = ec2.describe_instances(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': ['running', 'stopped', 'terminated']
            }]
        )

        all_instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']

                all_instances.append((instance_id, state))

        # Display
        if not all_instances:
            print("No instances found.")
        else:
            print("Instance IDs with their current state:\n")
            for instance_id, state in all_instances:
                print(f"🆔 {instance_id} → {state.upper()}")

    except Exception as e:
        print(f"❌ Error fetching instances: {e}")

# Run the function
list_instance_ids()
