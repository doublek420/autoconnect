"""
Tests for this project...

Copyright (C) 2001-2007 Oisin Mulvihill.            
Email: oisin.mulvihill@gmail.com
                                                                   
This library is free software; you can redistribute it and/or        
modify it under the terms of the GNU Lesser General Public           
License as published by the Free Software Foundation; either        
version 2.1 of the License, or (at your option) any later version.    
                                                                   
This library is distributed in the hope that it will be useful,       
but WITHOUT ANY WARRANTY; without even the implied warranty of        
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU      
Lesser General Public License for more details.     
                                                                   
You should have received a copy of the GNU Lesser General Public
License along with this library (see the file LICENSE.TXT); if not,
write to the Free Software Foundation, Inc., 59 Temple Place,
Suite 330, Boston, MA 02111-1307 USA.            
                                                                   
"""
import os
import sys
import socket
import unittest

import autoconnect



class AutoConnectTests(unittest.TestCase):
    
    open_ports = []
    
    def tearDown(self):
        # close any open sockets:
        for sock in self.open_ports:
            sock.close()


    def testRandomPorts(self):
        """Test the random_ports() function.
        """
        self.assertEquals(len(autoconnect.random_ports()), 15)
        self.assertEquals(len(autoconnect.random_ports(2)), 2)
        

    def testIsFree(self):
        """Test the is_free() port.
        """
        inuse_port = 12193
        free_port = 12199

        # bind to the port we're going to test against:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.bind(('', inuse_port))
        except socket.error, e:
            raise ValueError("The testing port %d isn't free" % inuse_port)
        self.open_ports.append(s)

        # Check the port isn't free for use:
        self.assertEquals(autoconnect.is_free(inuse_port), False, "In use port wasn't tested as being used!")
        

        # Hold the port I want to test is free busy until I want to use it.
        s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s2.bind(('', free_port))
        except socket.error, e:
            raise ValueError("The testing port %d isn't free" % free_port)

        # Check the free port is tested as being free:
        s2.close()
        self.assertEquals(autoconnect.is_free(free_port), True, "Free port wasn't tested as being free!")
        
        
    
    def testRandomFreePort(self):
        """Test the get_random_port() and its checking of the free port.
        """
        # Test I get an exception when there are no more free ports.
        retries = 1
        port = 12123

        # bind to the port we're going to test against:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', port))
        self.open_ports.append(s)
        
        self.assertRaises(autoconnect.FreePortError, autoconnect.get_free_port, testing=(retries, port))
        
        # Now try again this time letting it retry more then once.
        retries = 2
        port = 0 # allows it to use random ports.
        free_port = autoconnect.get_free_port(testing=(retries, port))

        # Try to bind to the free port after getting it:
        s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s2.bind(('', free_port))
        self.open_ports.append(s2)


    def testClientToServerConnect(self):
        """Test the client receive of a server broadcast.
        """
        import sys
        import nose
        if sys.platform.startswith("linux"):
            raise nose.SkipTest("Skipping this test on linux, I need to do it differently.")
            
        common_port = autoconnect.get_free_port()
        test_information = "Hello! This is some information. Connect on URL http://www.example.com:80/"
        
#        b = autoconnect.broadcaster.UdpBroadcaster(broadcast_address='127.0.0.1', broadcast_period=1)
        b = autoconnect.broadcaster.UdpBroadcaster(broadcast_period=1)
        b.start(test_information, [common_port])
        
        r = autoconnect.receiver.UdpReceiver()
#        data, address = r.receive(common_port, interface='127.0.0.1', timeout="20")
        data, address = r.receive(common_port, timeout="20")
        b.stop()
        
        self.assertEquals(data, test_information)


    