#!/usr/bin/env python3
# This script uploads a plugin package on the server
#
# Author: A. Pasotti, V. Picavet

import sys
import getpass
import os
from optparse import OptionParser
from xmlrpc import client
from django.core.files.uploadedfile import SimpleUploadedFile

# Configuration
PROTOCOL = 'http'
SERVER = 'plugins.qgis.org'
PORT = '80'
ENDPOINT = '/plugins/RPC2/'
VERBOSE = False


def main(options, args):
    address = "%s://%s:%s@%s:%s%s" % (
        PROTOCOL, options.username, options.password,
        options.server, options.port, ENDPOINT)
    print("Connecting to: %s" % hidepassword(address))
    server = client.ServerProxy(address, verbose=VERBOSE)
    try:
        with open(args[0], "rb") as file:
            uploaded_file = SimpleUploadedFile(
                args[0], file.read(),
                content_type="application/zip")
        plugin_id, version_id = server.plugin.upload(
            client.Binary(open(args[0], 'rb').read()))
        print("Plugin ID: %s" % plugin_id)
        print("Version ID: %s" % version_id)
    except client.ProtocolError as err:
        print("A protocol error occurred")
        print("URL: %s" % hidepassword(err.url, 0))
        print("HTTP/HTTPS headers: %s" % err.headers)
        print("Error code: %d" % err.errcode)
        print("Error message: %s" % err.errmsg)
    except client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)


def hidepassword(url, start=6):
    """Returns the http url with password part replaced with '*'."""
    passdeb = url.find(':', start) + 1
    passend = url.find('@')
    return "%s%s%s" % (url[:passdeb], '*' * (passend - passdeb), url[passend:])


if __name__ == "__main__":
    parser = OptionParser(usage="%prog [options] plugin.zip")
    parser.add_option("-w", "--password", dest="password",
                      help="Password for plugin site", metavar="******")
    parser.add_option("-u", "--username", dest="username",
                      help="Username of plugin site", metavar="user")
    parser.add_option("-p", "--port", dest="port",
                      help="Server port to connect to", metavar="80")
    parser.add_option("-s", "--server", dest="server",
                      help="Specify server name", metavar="plugins.qgis.org")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print("Please specify zip file.\n")
        parser.print_help()
        sys.exit(1)
    if not options.server:
        options.server = SERVER
    if not options.port:
        options.port = PORT
    env_username = os.environ.get('OSGEO_QGIS_USERNAME')
    if env_username is None:
        if not options.username:
            # interactive mode
            username = getpass.getuser()
            print("Please enter user name [%s] :" % username,)
            res = input()
            if res != "":
                options.username = res
            else:
                options.username = username
    else:
        options.username = env_username
    env_password = os.environ.get('OSGEO_QGIS_PASSWORD')
    if env_password is None:
        if not options.password:
            # interactive mode
            options.password = getpass.getpass()
    else:
        options.password = env_password
    main(options, args)
