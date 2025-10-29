import boto3


aws_m_c = boto3.session.Session(profile_name="default", region_name="eu-north-1")
ec2 = aws_m_c.client("ec2")

# def terminate_instance(instance_id):

#     # ec2 = boto3.client('ec2', region_name='eu-north-1')  # or your region
#     try:
#         response = ec2.terminate_instances(InstanceIds=[instance_id])
#         print(f"Instance {instance_id} termination initiated.")
#         for state in response['TerminatingInstances']:
#             print(f"Current state: {state['CurrentState']['Name']}")
#     except Exception as e:
#         print(f"Error terminating instance {instance_id}: {e}")
# terminate_instance('i-02aa0d55c2cd7a80b')


def stop_instances(instance_id):

    # ec2 = boto3.client('ec2', region_name='eu-north-1')  # or your region
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} stopping initiated.")
        for state in response['StoppingInstances']:
            print(f"Current state: {state['CurrentState']['Name']}")
    except Exception as e:
        print(f"Error stopping instance {instance_id}: {e}")
stop_instances('i-03bfbe029255cffc0')