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
import doc
import util
import example
import receiver
import broadcaster

from receiver import watch
from receiver import UdpReceiver
from broadcaster import beacon
from broadcaster import UdpBroadcaster
from util import is_free
from util import random_ports
from util import FreePortError
from util import get_free_port
from util import AUTOCONNECT_RANGE


# Typo which refers to beacon. Will be removed in future.
from broadcaster import beckon


