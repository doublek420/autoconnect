"""
I wrote this module a while ago (5+ years) and though it would be handy
for others. Its a handy auto-socket connection module. I used it 
orginally in a internet cafe management system. The client installed
by the installer would start the receiver. It would then wait for the 
server to broadcast its URL and on receiving it connect and do its 
business.

Check out the example test_server.py and test_client.py for usage examples.

Running the test_server:
    oisin@snorky [autoconnect]> PYTHONPATH=lib/ python lib/autoconnect/example/test_server.py 
    Waiting for client to connect.
    Got a new client connection:  <socket._socketobject object at 0x57efc0> ('172.17.125.117', 54323)
    oisin@snorky [autoconnect]> 

Running the test_client:
    oisin@snorky [autoconnect]> PYTHONPATH=lib/ python lib/autoconnect/example/test_client.py 
    Waiting to receive a broadcast on port: 30000
    Received packet from ('172.17.125.126', 1477)
    Socket connected to server successfully:  ('172.17.125.126', 10000)
    Done, exiting now.
    oisin@snorky [autoconnect]> 

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
import time
import socket
import random


# Used by client and server in the auto connect negotiation process. 
# At least on of these will be free on the server and client:
AUTOCONNECT_RANGE = [5311, 29006, 25155, 22672, 14729, 35998, 11812, 4764, 26274, 21336, 27557, 37041, 38109, 17597, 23476]


class FreePortError(Exception):
    """Raised when I could not get a free port.
    """


def random_ports(number=15, min_port=2000, max_port=40001):
    """This function returns a random list of ports.
    
    This list of ports is hard coded into an app that wants
    to auto connect. Both client and server have the same
    list.
    
    Note: these ports aren't tested for availability.
    
    number:
        This is the amount of random port numbers to
        return.

    min_port, max_port:
        These are the range of ports over which to try
        and get a free port from. 
        
        Default: 2000 to 40000 inclusive.
        
    returned:
        [xyz, ...]
    
    """
    random_ports = []
    
    for i in range(0, number):
        random_ports.append(random.randint(min_port, max_port))
        
    return random_ports


def is_free(test_port):
    """Test if a given port number is free for use.
    
    test_port:
        This is the UDP port to test.
    
    returned:
        True: 
            Port is available for use.
        False
            Port not available.
                
    """
    returned = True
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client_socket.bind(('', test_port))
        client_socket.close()
        
    except socket.error, e:
        returned = False
    
    return returned



def get_free_port(min_port=2000, max_port=40001, testing=None):
    """Test and return a free port on the machine in the range 2000, 40000.

    min_port, max_port:
        These are the range of ports over which to try
        and get a free port from. 
        
        Default: 2000 to 40000 inclusive.

    testing:
        (retries, port)

        This is used to unit test this function.

    Note: 
        If a free port cannot be recovered after 100 retires
        then FreePortError will be raised. This prevents looping
        forever if there are network errors preventing testing.
        
    Returned:
        The number of a UDP port which is available for use.

    """
    retries = 100
    test_port = None
    next_port = random.randint
        
    if testing:
        retries = testing[0]
        if testing[1]:
            # Greater then zero means use the fixed port given.
            next_port = lambda x,y: testing[1]
        
    while retries:
        retries -= 1
        test_port = next_port(min_port, max_port)
        #print "test_port: ", test_port
        if is_free(test_port):
            break
        else:
            # Port isn't free. Try another.
            test_port = None
            time.sleep(0.1) # wait a bit

    if not test_port:
        raise FreePortError("I was unabled to get a free UDP port!")

    #print "rc: ", test_port
    return test_port
        

    





