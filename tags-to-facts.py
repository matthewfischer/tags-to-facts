#!/usr/bin/python

import sys
import socket
from landscape_api.base import API, HTTPError

# requires the landscape api package
# sudo add-apt-repository ppa:landscape/landscape-api
# sudo apt-get update
# sudo apt-get install landscape-api

# NOTE: On Ubuntu server you'll need python-software-properties
# to get add-apt-repository installed

uri = "https://landscape.canonical.com/api/"
# XXX push to hiera
key = "FILLIN"
secret = "FILLIN"
api = None
tag_prefix = "landscape_tag"
DEBUG = False

def main():
    global api
    api = API(uri, key, secret)
    computer = find_this_host()
    if computer:
        return_tags(computer)

def find_this_host():
    try:
        computers = get_computers(query=socket.gethostname())
        if len(computers) == 0:
            print >> sys.stderr, "No computers found"
            sys.exit(1)
        elif len(computers) == 1:
            return computers[0]
        else:
            print >> sys.stderr, "Too many computers matched"
            sys.exit(1)

    except Exception, e:
        print >> sys.stderr, "Exception: %s" % e
        sys.exit(1)

def return_tags(computer):
    if not computer['tags']:
        print sys.stderr, "No tags found, skipping %s" % computer['id']
        sys.exit(1)
    i = 0
    for t in computer['tags']:
        print "%s%d=%s" % (tag_prefix, i,t)
        i+=1

def get_computers(query):
    try:
        computers = api.get_computers(query)
    except HTTPError, e:
        print sys.stderr, ("\nGot server error:\n"
                "Code: %d\n"
                "Message: %s\n") % (e.code, e.message)
        return []

    if DEBUG:
        for computer in computers:
            print "Id: %s, Hostname: %s" % (computer['id'],
                computer['hostname'])

    return computers

if __name__ == "__main__":
    main()
