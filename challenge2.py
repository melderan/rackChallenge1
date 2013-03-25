'''
Challenge 2 - Python
Write a script that clones a server (takes an image and deploys the image as a new server).
'''

# Import Pyrax library
import pyrax

# Set Authentication File
pyrax.set_credential_file("/home/melderan/.rackspace_cloud_credentials")
# Authenticate and get Cloud Servers handle
cs = pyrax.cloudservers

# Get the API server object
srv = [s for s in cs.servers.list() if 'API' in s.name][0]

# Make an image for this server
srv.create_image(srv.name + '-Challenge2')

# Get image object
img = [i for i in cs.images.list() if '-Challenge2' in i.name][0]

# Get flavor ID of image
flv = [i for i in cs.flavors.list() if i.ram == img.minRam][0]

# Wait till image is done
while 'ACTIVE' not in img.status:
    img = [i for i in cs.images.list() if '-Challenge2' in i.name][0]

# Now that the image is done, do the same from challenge 1

# Number of server to make
numNewServersToMake = 1

# Make the servers and store the objects in a list
srv = cs.servers.create(srv.name + '-Copy', img.id, flv.id)

# Get Admin Passwords as they are only in this first object
password = srv.adminPass

# Lets test the server until its Active
while 'ACTIVE' not in srv.status:
    srv = cs.servers.get(srv.id)

# server should be active now, print details
print srv.name, '--',
for addr in srv.networks['public']:
    if '.' in addr:
        print addr, '--',
print password
