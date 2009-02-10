#
#   test_server.py
#
#   Copyright (C) 2001-2007 Oisin Mulvihill.
#   Email: oisin.mulvihill@gmail.com
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library (see the file LICENSE.TXT); if not,
#   write to the Free Software Foundation, Inc., 59 Temple Place,
#   Suite 330, Boston, MA 02111-1307 USA.
#
#   Date: 2001/12/06 15:54:30
#
import sys
import socket
import xmlrpclib
import autoconnect
from SimpleXMLRPCServer import SimpleXMLRPCServer


class Person:
    
    def greet(self, name=''): 
        msg = "Hello, nice to meet you"
        if name:
            msg = "%s %s" % (msg, name)
        return msg


class Server:
    """This server runs a simple XML-RPC server and its clients
    automatically find it. Its magic ;)     
    """
    def __init__(self):
        self.server = None
        self.broadcaster = None


    def main(self):
        print "Starting XML-RPC server http://localhost:8000"
        self.server = SimpleXMLRPCServer(("localhost", 8000))
        self.server.register_instance(Person())

        # Start the beckon to tell clients the servers XML-RPC URI:
        print "Homing beacon running. Press Ctrl-C to exit."
        self.broadcaster = autoconnect.beacon("http://localhost:8000")        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt,e:
            pass
            self.server.server_close()




if __name__  == '__main__':
    server = Server()
    server.main()   
