'''
Challenge 2 - Python
Write a script that clones a server (takes an image and deploys the image as a new server).
'''

# Import Libraries
import pyrax                    # Rackspace API
import time                     # Time lib for sleep(seconds)
import argparse                 # Argument Parser Library
from os.path import expanduser  # Expands '~' for user home folder

# Setup our argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--credentials', help="Specify Credentials file.", type=str, default='~/.rackspace_cloud_credentials')
parser.add_argument('-i', '--imageName', help="Specify image name to create.", type=str, default='-Challenge2')
parser.add_argument('-p', '--prepend', help="Prepend current server name to image", action='store_true')
parser.add_argument('-a', '--alterFlavor', help="Flag to adjust new servers flavor. Use with -f", action='store_true')
parser.add_argument('-f', '--flavor', help="Amount of RAM to be given to the server. Must use with -a", type=int)
parser.add_argument('-s', '--serverName', help="The name of the server to take image of.", type=str, default='API')
parser.add_argument('-n', '--number', help="Number of new Cloud Servers to build from image.", type=int, default=1)
args = parser.parse_args()

# Test if alterFlavor and flavor were used correctly
if (args.alterFlavor) == (args.flavor is None):
    print 'You failed to use -a and -f correctly.  Please use -h for help'
    exit();

# Set Authentication File
pyrax.set_credential_file(expanduser(args.credentials))

# Authenticate and get Cloud Servers handle
cs = pyrax.cloudservers

# Get the API server object
srv = [s for s in cs.servers.list() if args.serverName in s.name][0]

# Find out what we are going to call the server
if args.prepend:
    imgName = srv.name + args.imageName
else:
    imgName = args.imageName

# Make an image of the server
srv.create_image(imgName)

# Get image object
img = [i for i in cs.images.list() if imgName in i.name][0]

# Get Flavor id
if args.alterFlavor and args.flavor >= img.minRam:
    flv = [i for i in cs.flavors.list() if i.ram == args.flavor][0]
else:
    flv = [i for i in cs.flavors.list() if i.ram == img.minRam][0]

# if they did choose an invalid flavor size let them know.
if args.flavor < img.minRam:
    print 'The flavor size chosen was {}.  You specified a new flavor smaller than required.'.format(img.minRam)

# Wait till image is done
while 'ACTIVE' not in img.status:
    time.sleep(60)
    img = [i for i in cs.images.list() if imgName in i.name][0]

# Now that the image is done, do the same from challenge 1

# Base server number
newServerNumberBase = len([s for s in cs.servers.list() if srv.name + '-Clone-' in s.name])

# Number of server to make
numNewServersToMake = args.number

# Make the servers and store the objects in a list
newServers = [cs.servers.create(srv.name + '-Clone-' + str(newServerNumberBase + i), img.id, flv.id) for i in xrange(numNewServersToMake)]

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
