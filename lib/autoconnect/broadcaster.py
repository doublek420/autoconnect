"""

UdpBroadcaster.py

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
import thread
import socket
import threading

import util


class UdpBroadcaster:
    """This class is used to broadcast some information to all machines on a LAN.

    The broadcast is by default every ten seconds or so however 
    this can be changed by the user. The broadcaster can also 
    send to a range of ports specified in the port_list provided to
    it. The UdpReceiver class is designed to receive broadcasts from
    this class
    
    """
    def __init__(self, broadcast_address='255.255.255.255', broadcast_period=10):
        """Do Setup.
                
        broadcase_address: 
            For LAN broadcast as far as the first router you can use
            255.255.255.255
            
        broadcast_period:
            Amount of time in seconds between broadcasts.
        
        """
        self.threadRunning = 0
        self.__broadcastAddress = broadcast_address
        self.__exitLock = threading.Event()
        self.__broadcastPeriod = broadcast_period 


    def __broadcaster(self, information, port_list):
        """This thread broadcasts the "information" to a list of port numbers in the LAN.
        """
        # Create the UDP socket.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Allow the socket to broadcast, set the socket options.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
#        print "Running"

        # Loop broadcasting until we're told to exit.
        while not self.__exitLock.isSet():
            # Send to all the ports in the list.
            for port in port_list:
                # Send the infomation.
#                print "Broadcast: ", (self.__broadcastAddress, port)
                server_socket.sendto(information, (self.__broadcastAddress, port))
            # Sleep before broadcasting again.
            time.sleep(self.__broadcastPeriod)

        # Done.
        server_socket.close()
        self.__exitLock.clear()
        self.threadRunning = 0


    def start(self, information, port_list):
        """Start the broadcasting thread using the information and port_list.

        This function will return if the thread is already running.
        """
        if self.threadRunning == 0:
            thread.start_new_thread(self.__broadcaster, (information, port_list))
            self.threadRunning = 1

        
    def stop(self):
        """Stop the broadcasting thread if its running.
        """
        # Set the exit event which will tell the broadcaster thread to exit.
        self.__exitLock.set()
        # wait for a bit.
        time.sleep(self.__broadcastPeriod)


    def __del__(self):
        """Set the exit flag to stop the broadcaster thread if its running.
        """
        try:
            # Try doing stop.
            self.stop()
        except:
            # Stop already called
            pass


def beacon(uri, port_range=util.AUTOCONNECT_RANGE):
    """Send out the server's URL

    uri:
        This is the server uri to broadcast on. This could
        be any string really, as long as its meaningfull to
        the client. This is the string that the watch()
        function will return.

    Returned:
       This returns a started instance of UdpBroadcaster.
       You'll need to call stop() when you've finished
       broadcasting.
        
    """
    broadcaster = UdpBroadcaster()
    broadcaster.start(uri, port_range)

    return broadcaster


# Kept for backwards compatiblity:
beckon = beacon
