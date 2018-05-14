import libcloud3

aws_connection = libcloud3.connect('aws', *myconnectionparameters)

ec2_instances = aws_connection.Ec2Instance.list()
