'''
Challenge 3 - Python
Write a script that accepts a directory as an argument as well as a container
name.  The script should upload the contents of the specified directory to
the container (or create it if it doesn't exist). The script should handle
errors appropriately. (Check for invalid paths, etc.)
'''


# Import Libraries
import pyrax                    # Rackspace API
import argparse                 # Argument Parser
import time                     # Time lib for sleep(seconds)
from os.path import expanduser  # Expands '~' for user home folder
from os.path import exists      # To test path input

# Authenticate to Rackspace
pyrax.set_credential_file(expanduser('~/.rackspace_cloud_credentials'))

# Setup our argument parser
parser = argparse.ArgumentParser()
parser.add_argument('localPath', help='Path to local files that will be uploaded to Cloud Files', type=str)
parser.add_argument('container', help='Name of Cloud Files Container to user (and/or create)', type=str)
args = parser.parse_args()

# check to see if the path given exists
if (not exists(args.localPath)):
    print 'You did not input a valid local path'
    exit(1)

# Get our Cloud Files handle
cf = pyrax.cloudfiles

# check to see if we have a container already and if not make one and get the handle
if args.container not in cf.list_containers():
    cont = cf.create_container(args.container)
else:
    cont = [c for c in cf.get_all_containers() if c.name == args.container][0]

print 'Begin Transfer: '
upload_key, totalSize = cf.upload_folder(args.localPath, container=(cont.name))
transfer = cf.get_uploaded(upload_key)
while transfer < totalSize:
    print '.',
    transfer = cf.get_uploaded(upload_key)
print 'Done'
