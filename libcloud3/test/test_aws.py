from libcloud3.drivers.aws import AWSDriver
import os

def test_instance_list():
    """Verify that we can instantiate an AWSDriver that lists EC2 instances"""

    aws = AWSDriver(access_key=os.environ.get('AWS_ACCESS_KEY'), access_secret=os.environ.get('AWS_ACCESS_SECRET'))
    aws.instances.get('us-east-1')
