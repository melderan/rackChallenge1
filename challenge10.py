'''
Challenge 10 - Python
Write an application that will:
- Create 2 servers, supplying a ssh key to be installed at /root/.ssh/authorized_keys.
- Create a load balancer
- Add the 2 new servers to the LB
- Set up LB monitor and custom error page. 
- Create a DNS record based on a FQDN for the LB VIP. 
- Write the error page html to a file in cloud files for backup.
** Will use 1 positional argument for key_file - Path to key file to upload **
'''
# Grabbing most of the code from Challenge 8

# Import Libraries
import time
import argparse
import pyrax
from os.path import expanduser

# Setup our argument parser
parser = argparse.ArgumentParser()
parser.add_argument('key_file', help='Path to public ssh key', type=str)
args = parser.parse_args()

# Set Authentication File for Pyrax
pyrax.set_credential_file(expanduser('~/.rackspace_cloud_credentials'))

# Do Auth and get some
cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
dns = pyrax.cloud_dns
cf = pyrax.cloudfiles

# Get contents of the key_file to upload to the server
try:
	fh = open(args.key_file, 'r')
	key = fh.read()
	fh.close()
except:
	print 'You need to provide a valid SSH Public Key'
	exit(1)

## Create 2 servers and get their data stored so we can build a load balancer and attach them to it.

# Get the Image and Flavor (CentOS 6.3 512MB)
imgID = [img for img in cs.images.list() if 'CentOS 6.3' in img.name][0].id
flvID = [flv for flv in cs.flavors.list() if 512 == flv.ram][0].id

numNewServers = 2
baseName = 'LB-Web'

# Make the files Dict for passing to the built servers
srv_files = {"/root/.ssh/authorized_keys": key}

# Make the servers and store the objects in a list
newServers = [cs.servers.create(baseName + str(i + 1), imgID, flvID, files=srv_files) for i in xrange(numNewServers)]

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
lb = clb.create("Challenge_10", port=80, protocol="HTTP", nodes=clbNodes, virtual_ips=[clbVip])

# Lets wait till the LB is done
while 'ACTIVE' not in lb.status:
    lb = clb.get(lb.id)
    time.sleep(30)

# Set domain name
domainName = 'wilylight.info'
# Make the DNS record
domain = [dom for dom in dns.get_domain_iterator() if domainName in dom.name][0]

# Record to add
record = [{
	"type":"A",
	"name":"challenge10.wilylight.info",
	"data":clbVip
}]

# Add it
dns.add_records(domain, record)

# Add a load balancer health monitor
lb.add_health_monitor(type="CONNECT", delay=10, timeout=10, attemptsBeforeDeactivation=3)

# Add a customer error page
html = '<html><head><title>Challenge10 - Error!</title></head><body><h1>This is normal.  Challenge10 says so!</h1></body></html>'
lb.set_error_page(html)

# Write it to a file and upload it to cloud files
with open('challenge10-error_page.html','w') as fh:
	fh.write(html)
cont = cf.create_container('Challenge10')
cont.upload_file('challenge10-error_page.html')

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