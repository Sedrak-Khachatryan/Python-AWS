import boto3
ec2 = boto3.resource('ec2')

# Create a new EC2 instance
instances = ec2.create_instances(
    ImageId='ami-0518bb0e75d3619ca',
    MinCount=1,
    MaxCount=2,
    InstanceType='t2.micro',
    KeyName='ec2-keypair.pem'
)