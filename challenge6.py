'''
Challenge 6 - Python
Write a script that creates a CDN-enabled container in Cloud Files.
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

# Get the handle for the DBaaS
cf = pyrax.cloudfiles

# Create a Challenge6 container
cont = cf.create_container('Challenge6')

# lets make this dude public... shall we...
cf.make_container_public(cont.name, ttl=900)

# lets get all the needed information such as the HTTP/S, Streaming, IOS
print "your freshly created CDN Enabled Cloud Files Container Information"
print "cdn_enabled", cont.cdn_enabled
print "cdn_ttl", cont.cdn_ttl
print "cdn_log_retention", cont.cdn_log_retention
print "cdn_uri", cont.cdn_uri
print "cdn_ssl_uri", cont.cdn_ssl_uri
print "cdn_streaming_uri", cont.cdn_streaming_uri
