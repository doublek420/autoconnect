#
"""
UdpReceiver.py

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
import socket
import random

import util


class UdpReceiver:
    """This class is used to receive a broadcast from the UdpBroadcaster class.
    """
    def __init__(self, receive_block_size=2048):
        """
        receive_block_size:
            The amount of bytes we should receive at a time.
        
        """
        self.receiveBlockSize = receive_block_size

    
    def receive(self, port, interface='', timeout=0):
        """This opens a udp port, waits to receive up to self.receiveBlockSize
        bytes. Then returns the data and address of who we received from
        and close the open udp port.
            
            port:
                The UDP port to listen for broadcasts on.

            interface:
                The physical interface to bind to.
            
            timeout:
                The amount of time (in seconds) to wait before giving up.
                If this is 0 then no timeout will be set and receive will
                block waiting for data.
        
        Returned:
            (Received Data, Socket Address)
        
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.bind((interface, port))
        
        if timeout:
            client_socket.settimeout(float(timeout))
        
        try:
            data, addr = client_socket.recvfrom(self.receiveBlockSize)
        finally:
            client_socket.close()
            
        return data, addr


class WatchError(Exception):
    """Raised when I get a timeout for or problem doing a watch.
    """


def watch(port_range=util.AUTOCONNECT_RANGE, timeout=60, retries=20):
    """Watch for the server beacon, which will tell use the URI we're to connect to.

    port_range:
        This is a random list of ports that are common
        to both the client and the server. By default the
        hard code list AUTOCONNECT_RANGE is used.
    
    timeout:
        The amount of time before we give up waiting for
        data on the selected random port.
        
    retries:
        The amount of times we watch for beacon broadcasts
        before we give up waiting.

        If this is 0 then the watch will wait indefinetly for
        a server broadcast.
        
    returned:
        The string containing a URI from the server. For
        example 'http://localhost:9384/rpc2'.
        
        This string can be anything the server wants to 
        send really. The only limit is the UdpReceiver
        block size and the physical UDP packet size limit.
        
    """
    uri = None
    current_retries = retries
    
    # Find a free port we'll watch for a beacon on:
    if current_retries == 0:
        # I need to give up on this if I can't get a free port.
        retries = 20
        
    while True:
        port = random.choice(port_range)
        if util.is_free(port):
            break
        else:
            retries -= 1            
            if not retries:
                raise WatchError("I was unable to find a free port in %s!" % port_range)
        time.sleep(0.1)

    # Loop watching for the server beacon:
    if current_retries:
        retries = current_retries
    else:
        # loop forever in the following loop as we don't
        # decrement retries when current_retries is 0
        retries = 1
    
    r = UdpReceiver()
            
    while retries:
        try:
            #print "watching on port %d..." % port
            uri, addr = r.receive(port, timeout=60)
            break
            
        except socket.error, e:
            uri = None
            if current_retries:
                # on decrement when currnt retries is not zero
                retries -= 1
            
    if not uri:
        raise WatchError("I was unable to see a server beacon!")
    
    return uri
        
    
