'''
Challenge 1 - Python
Write a script that builds three 512 MB Cloud Servers that following a similar naming convention.
(ie., web1, web2, web3) and returns the IP and login credentials for each server. Use any image you want.
'''

# Import Libraries
import pyrax                    # Rackspace API
import time                     # Time lib for sleep(seconds)
import argparse                 # Argument Parser Library
from os.path import expanduser  # Expands '~' for user home folder

# Setup our argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--credentials', help="Specify Credentials file.", type=str, default='~/.rackspace_cloud_credentials')
parser.add_argument('-i', '--image', help="Specify image ID to build servers from.", type=str, default='Arch')
parser.add_argument('-f', '--flavor', help="Amount of RAM to be given to the server.", type=int, default=512)
parser.add_argument('-s', '--serverName', help="The base name that all the created servers will share.", type=str, default='Challenge1-')
parser.add_argument('-n', '--number', help="Number of new Cloud Servers to build.", type=int, default=3)
args = parser.parse_args()

# Set Authentication File
pyrax.set_credential_file(expanduser(args.credentials))
# Authenticate and get Cloud Servers handle
cs = pyrax.cloudservers

# Check if -i or --image were used
if args.image == 'Arch':
    imgID = [img for img in cs.images.list() if 'Arch' in img.name][0].id
else:
    imgID = args.image

# Get the Flavor id from Flavor Object for args.flavor
flvID = [flv for flv in cs.flavors.list() if flv.ram == args.flavor][0].id

# Base server name from args
newServerNameBase = args.serverName

# Base server number
newServerNumberBase = len([srv for srv in cs.servers.list() if newServerNameBase in srv.name])

# Number of server to make
numNewServersToMake = args.number

# Make the servers and store the objects in a list
newServers = [cs.servers.create(newServerNameBase + str(newServerNumberBase + i), imgID, flvID) for i in xrange(numNewServersToMake)]

# Get Admin Passwords as they are only in this first object
passwords = [srv.adminPass for srv in newServers]

# Make a list to test each server for completeness
complete = [False for i in xrange(numNewServersToMake)]

# Lets test each server until they are all Active
while False in complete:
    for srvNum in xrange(numNewServersToMake):
        srv = cs.servers.get(newServers[srvNum])
        if 'ACTIVE' in srv.status:
            complete[srvNum] = True
        newServers[srvNum] = srv
    time.sleep(60)

# Each server should be active now, print details
for i in xrange(numNewServersToMake):
    srv = newServers[i]
    print srv.name, '--',
    for addr in srv.networks['public']:
        if '.' in addr:
            print addr, '--',
    print passwords[i]
