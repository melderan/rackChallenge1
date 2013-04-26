'''
Challenge 8 - Python
Write a script that will create a static webpage served out of Cloud Files.
The script must create a new container, cdn enable it, enable it to serve an 
index file, create an index file object, upload the object to the container, 
and create a CNAME record pointing to the CDN URL of the container.
'''

# Import Libraries
import pyrax                    # Rackspace API
import time                     # Time lib for sleep(seconds)
import argparse                 # Argument Parser Library
from os.path import expanduser  # Expands '~' for user home folder

# Not implemented. Copied from Challenge1
## Setup our argument parser
#parser = argparse.ArgumentParser()
#parser.add_argument('-c', '--credentials', help="Specify Credentials file.", type=str, default='~/.rackspace_cloud_credentials')
#parser.add_argument('-i', '--image', help="Specify image ID to build servers from.", type=str, default='Arch')
#parser.add_argument('-f', '--flavor', help="Amount of RAM to be given to the server.", type=int, default=512)
#parser.add_argument('-s', '--serverName', help="The base name that all the created servers will share.", type=str, default='Challenge1-')
#parser.add_argument('-n', '--number', help="Number of new Cloud Servers to build.", type=int, default=3)
#args = parser.parse_args()

# Set Authentication File
pyrax.set_credential_file(expanduser('~/.rackspace_cloud_credentials'))

# Get Handle to DNS and CF
dns = pyrax.cloud_dns
cf = pyrax.cloudfiles

# Make a public container
cont = cf.create_container('Challenge8')
cf.make_container_public(cont.name, ttl=900)

# Set the index page to index.html
cont.set_web_index_page('index.html')

# Create a simple index.html page to upload
with open('index.html','w') as fh:
    fh.write('<html><head><title>Challenge 8</title></head><body><p>This is the index page of Challenge 8.</p></body></html>')

# Upload the file to Cloud Files
cont.upload_file('index.html')

# Get container CDN url
url = cont.cdn_uri

# Grab our domain object for wilylight.info
domain = [dom for dom in dns.get_domain_iterator() if 'wilylight' in dom.name][0]

# Build our new record
record = [{
        "type":"CNAME",
        "name":"Challenge8.wilylight.info",
        "data":url}]

# Add him to DNS
print dns.add_records(domain, record)
