'''
Challenge 9 - Python
Write an application that when passed the arguments FQDN, image, and flavor
it creates a server of the specified image and flavor with the same name as
the fqdn, and creates a DNS entry for the fqdn pointing to the server's public IP.
'''
# Import Libraries
import time
import argparse
import pyrax
from os.path import expanduser

# Setup our argument parser
parser = argparse.ArgumentParser()
parser.add_argument('FQDN', help='Fully Qualified Domain Name (i.e. test.example.com)', type=str)
parser.add_argument('Image', help='Image ID to build server from', type=str)
parser.add_argument('Flavor', help='Flavor ID to build server as', type=str)
args = parser.parse_args()

# Authenticate to Pyrax
pyrax.set_credential_file(expanduser('~/.rackspace_cloud_credentials'))

# Get our handle to cloud dns and cloud servers
cs = pyrax.cloudservers
dns = pyrax.cloud_dns

# Create the server
srv = cs.servers.create(args.FQDN, args.Image, args.Flavor)

# Get the servers password
password = srv.adminPass

# Wait for Server to be done
while 'ACTIVE' not in srv.status:
    srv = cs.servers.get(srv.id)
    time.sleep(60)

# Get public address
ip_add = ''
for net in srv.networks['public']:
    if '.' in net:
        ip_add = net

# Parse input FQDN and try and get closest leaf/root domain name
inputFQDN = args.FQDN
leaf = '.'.join(inputFQDN.split('.')[1:])

# now that we know the leaf lests
domains = [dom for dom in dns.get_domain_iterator() if leaf in dom.name]

if len(domains) != 1:
    print 'You do not have a properly created subdomain setup for this domain: {}'.format(leaf)
    exit(1)

# Build the record for DNS
record = [{
         "type":"A",
         "name":args.FQDN,
         "data":ip_add}]

# Make the Record and give the admin password to console
print dns.add_records(domains[0], record)
print args.FQDN, '--', ip_add, '--', password
print 'Please remember to wait for the DNS record to propagate'
