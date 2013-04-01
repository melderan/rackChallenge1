'''
Challenge 1 - Python
Write a script that builds three 512 MB Cloud Servers that following a similar naming convention.
(ie., web1, web2, web3) and returns the IP and login credentials for each server. Use any image you want.
'''

# Import Libraries
import pyrax                    # Rackspace API
import time                     # Time lib for sleep(seconds)
from os.path import expanduser  # Expands '~' for user home folder

# Set Authentication File
pyrax.set_credential_file(expanduser("~/.rackspace_cloud_credentials"))
# Authenticate and get Cloud Servers handle
cs = pyrax.cloudservers

# Get the Image id from Image Object for 'Arch'
imgID = [img for img in cs.images.list() if 'Arch' in img.name][0].id

# Get the Flavor id from Flavor Object for '512M'
flvID = [flv for flv in cs.flavors.list() if flv.ram == 512][0].id

# Base server name
newServerNameBase = "Arch-Challenge1-"

# Base server number
newServerNumberBase = len([srv for srv in cs.servers.list() if newServerNameBase in srv.name])

# Number of server to make
numNewServersToMake = 3

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
