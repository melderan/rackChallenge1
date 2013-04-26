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

# Set Authentication File for Pyrax
pyrax.set_credential_file(expanduser('~/.rackspace_cloud_credentials'))

# Do Auth and get some
cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers

## Create 2 servers and get their data stored so we can build a load balancer and attach them to it.

# Get the Image and Flavor (CentOS 6.3 512MB)
imgID = [img for img in cs.images.list() if 'CentOS 6.3' in img.name][0].id
flvID = [flv for flv in cs.flavors.list() if 512 == flv.ram][0].id

numNewServers = 2
baseName = 'LB-Web'

# Make the servers and store the objects in a list
newServers = [cs.servers.create(baseName + str(i + 1), imgID, flvID) for i in xrange(numNewServers)]

# Get Admin Passwords as they are only in this first object
passwords = [srv.adminPass for srv in newServers]

# Make a list to test each server for completeness
complete = [False for i in xrange(numNewServers)]

# Lets test each server until they are all Active
while False in complete:
    for srvNum in xrange(numNewServers):
        srv = cs.servers.get(newServers[srvNum])
        if 'ACTIVE' in srv.status:
            complete[srvNum] = True
        newServers[srvNum] = srv
    time.sleep(60)

# Now that the servers are complete, lets get a load balancer
# List of nodes
clbNodes = []
# Create a node for each server
for srv in newServers:
    srv_ip = srv.networks["private"][0]
    clbNodes.append(clb.Node(address=srv_ip, port=80, condition="ENABLED"))

# Generate a VIP
clbVip = clb.VirtualIP(type='PUBLIC')

# Make the LB
lb = clb.create("Challenge_7", port=80, protocol="HTTP", nodes=clbNodes, virtual_ips=[clbVip])

# Lets wait till the LB is done
while 'ACTIVE' not in lb.status:
    lb = clb.get(lb.id)
    time.sleep(30)

# Now everything should be good, Lets print out info
# LB - print details
print 'Load Balancer - Public IP:', clbVip
print 'Servers:'
# Server - print details
for i in xrange(numNewServers):
    srv = newServers[i]
    print srv.name, '--',
    for addr in srv.networks['public']:
        if '.' in addr:
            print addr, '--',
    print passwords[i]
