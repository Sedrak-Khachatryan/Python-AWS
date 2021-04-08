# ------------------------------------------------
# Program by Sedrak K.
#
#
#
# Version         Date              Info
#   1.0           2021        Inintial Version
#
# ------------------------------------------------

import boto3

ec2 = boto3.resource('ec2')

# create a file to store the key locally
outfile = open('ec2-keypair.pem','w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='ec2-keypair.pem')

# capture the key and store it ina  file
KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)