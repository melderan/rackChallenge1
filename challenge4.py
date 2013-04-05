'''
Challenge 4 - Python
Write a script that uses Cloud DNS to create a new A record when passed
a FQDN and IP address as arguments.
'''


# Import Libraries
import time
import argparse
import pyrax
from os.path import expanduser

# Setup our argument parser
parser = argparse.ArgumentParser()
parser.add_argument('FQDN', help='Fully Qualified Domain Name (i.e. test.example.com)', type=str)
parser.add_argument('IP', help='IP Address to associate name with (i.e. 166.57.4.122)', type=str)
args = parser.parse_args()

# Authenticate to Pyrax
pyrax.set_credential_file(expanduser('~/.rackspace_cloud_credentials'))

# Get our handle to cloud dns
dns = pyrax.cloud_dns

# Now I am going under the assumption that we will be building our nodes in a proper
# dns tree structure.  leaf.tree.root.tld  With this assumption I am going to try
# and place the corresponding FQDN into the proper domain container (or sub domain container)

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
            "data":args.IP}]

print dns.add_records(domains[0], record)
