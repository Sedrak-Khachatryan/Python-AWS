import boto3


ec2 = boto3.resource('ec2')


# Create Vpc
vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
vpc.create_tags(Tags=[{"Key": "Name", "Value": "default_vpc"}])
vpc.wait_until_available()
print(vpc.id)


# Create then attach internet gateway
ig = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
print(ig.id)


# Create a route table and a public route
route_table = vpc.create_route_table()
route = route_table.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ig.id
    )
print(route_table.id)


# Create Subnet
subnet = ec2.create_subnet(
    CidrBlock='192.168.1.0/24',
    VpcId=vpc.id
    )


# Create sec group
sec_group = ec2.create_security_group(
    GroupName='slice_0', Description='slice_0 sec group',
    VpcId=vpc.id
    )
sec_group.authorize_ingress(
    CidrIp='0.0.0.0/0',
    IpProtocol='icmp',
    FromPort=-1,
    ToPort=-1
    )


# Create instance
instances = ec2.create_instances(
    ImageId='ami-0518bb0e75d3619ca',
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    KeyName='ec2-keypair.pem',
    NetworkInterfaces=[
        {
            'SubnetId': subnet.id,
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'Groups': [sec_group.group_id]
        }
    ]
)
instances[0].wait_until_running()


# create a file to store the key locally
outfile = open('Output.txt', 'w')
description = {"VPC_ID": vpc.id,
               "Internet_Gateway_Id": ig.id,
               "Route_Table_Id": route_table.id,
               "Security_Group_Id": sec_group.id,
               "Instance_Id": instances[0].id
}

outfile.write(str(description))
