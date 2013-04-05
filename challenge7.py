'''
Challenge 7 - Python
Write a script that will create 2 Cloud Servers and add them as nodes to a new Cloud Load Balancer.
'''


# Import Libraries
import time
import argparse
import pyrax
from os.path import expanduser

# Not implemented Copied from Challenge5
# Setup our argument parser
#parser = argparse.ArgumentParser()
#parser.add_argument('FQDN', help='Fully Qualified Domain Name (i.e. test.example.com)', type=str)
#parser.add_argument('IP', help='IP Address to associate name with (i.e. 166.57.4.122)', type=str)
#args = parser.parse_args()

# Authenticate to Pyrax
pyrax.set_credential_file(expanduser('~/.rackspace_cloud_credentials'))

# Create 2 servers and get their data stored so we can build a load balancer and attach them to it.

