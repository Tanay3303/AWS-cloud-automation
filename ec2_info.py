from datetime import datetime, timedelta, timezone
import boto3

aws_m_c = boto3.session.Session(profile_name="default", region_name="eu-north-1")
ec2 = aws_m_c.client("ec2")

def list_running_instances():
    try:
        # Describe all instances
        response = ec2.describe_instances()
        print("\n Running EC2 Instances:\n")

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                state = instance['State']['Name']

                # Only show running instances
                if state == 'running':
                    instance_id = instance['InstanceId']
                    launch_time = instance['LaunchTime']  # UTC time
                    name = "No Name"


                    # Calculate uptime
                    now = datetime.now(timezone.utc)
                    uptime = now - launch_time
                    hours, remainder = divmod(uptime.total_seconds(), 3600)
                    minutes, _ = divmod(remainder, 60)

                    print(f"Instance Name : {name}")
                    print(f"Instance ID   : {instance_id}")
                    print(f"Launch Time   : {launch_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
                    print(f"Uptime        : {int(hours)} hours {int(minutes)} minutes\n")

    except Exception as e:
        print(f"Error listing instances: {e}")


list_running_instances()


