from libcloud3.drivers.aws import AWSDriver, EC2InstanceType
import os


def test_instance_list():
    """Verify that we can instantiate an AWSDriver that lists EC2 instances"""

    aws = AWSDriver(access_key=os.environ.get('AWS_ACCESS_KEY'), access_secret=os.environ.get('AWS_ACCESS_SECRET'))
    instances = aws.EC2Instance.get('us-east-1')

    assert isinstance(instances, list)
    assert instances[0].region == 'us-east-1'
    assert instances[0].id == instances[0].InstanceId


def test_instance_describe():
    """Verify that describing an instance returns a dict with EC2 attributes for this instance"""

    aws = AWSDriver(access_key=os.environ.get('AWS_ACCESS_KEY'), access_secret=os.environ.get('AWS_ACCESS_SECRET'))
    instances = aws.EC2Instance.get('us-east-1')

    assert isinstance(instances, list)

    i = instances[0].describe()

    assert isinstance(i, dict)
    assert i['InstanceId'] == instances[0].InstanceId


def test_instance_status():
    """Verify that we can get the status of an EC2 instance"""

    aws = AWSDriver(access_key=os.environ.get('AWS_ACCESS_KEY'), access_secret=os.environ.get('AWS_ACCESS_SECRET'))
    instances = aws.EC2Instance.get('us-east-1')

    assert isinstance(instances, list)

    i = instances[0].status()

    assert isinstance(i, dict)
    assert 'InstanceStatus' in i
    assert i['InstanceId'] == instances[0].InstanceId


def test_s3bucket_list():
    """Verify that we can instantiate an AWSDriver that lists S3 buckets"""

    aws = AWSDriver(access_key=os.environ.get('AWS_ACCESS_KEY'), access_secret=os.environ.get('AWS_ACCESS_SECRET'))
    buckets = aws.S3Bucket.get()

    assert isinstance(buckets, list)
    assert buckets[0].id == buckets[0].Name


def test_s3object_list():
    """Verify that we can instantiate an AWSDriver that lists S3 buckets"""

    aws = AWSDriver(access_key=os.environ.get('AWS_ACCESS_KEY'), access_secret=os.environ.get('AWS_ACCESS_SECRET'))
    buckets = aws.S3Bucket.get()
    obj = aws.S3Object.get(buckets[0].id)

    assert isinstance(buckets, list)
    assert obj.id == obj.Key
