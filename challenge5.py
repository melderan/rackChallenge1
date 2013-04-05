'''
Challenge 5 - Python
Write a script that creates a Cloud Database instance.
This instance should contain at least one database,
and the database should have at least one user that can connect to it.
'''


# Import Libraries
import time
import argparse
import pyrax
from os.path import expanduser

# Not implemented
# Setup our argument parser
#parser = argparse.ArgumentParser()
#parser.add_argument('FQDN', help='Fully Qualified Domain Name (i.e. test.example.com)', type=str)
#parser.add_argument('IP', help='IP Address to associate name with (i.e. 166.57.4.122)', type=str)
#args = parser.parse_args()

# Authenticate to Pyrax
pyrax.set_credential_file(expanduser('~/.rackspace_cloud_credentials'))

# Get the handle for the DBaaS
cdb = pyrax.cloud_databases

# Create a database instance
instance = cdb.create("Challenge5", flavor=512, volume=1)

# Wait for the instance to be completed
while 'ACTIVE' not in instance.status:
    instance = [inst for inst in cdb.list() if inst.id == instance.id][0]

# Create a database in that instance
db = instance.create_database("Challenge5")

# Create a user for this database
user = instance.create_user(name='melderan', password='Ch@ll3ng35', database_names=[db])

#print out all our info to the user
print 'Hostname:', instance.hostname
print 'Database Name:', db.name
print 'User:', user.name
print 'Password:', 'Ch@ll3ng35'
