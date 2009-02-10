#
#   test_client.py
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
#   Date: 2001/12/06 17:23:28
#
import xmlrpclib

import autoconnect


def main():
    """Watch for server beckons the connect and use the XML-RPC Server.
    """
    print "Watching for the server beacon."
    uri = autoconnect.watch()

    print "Got the server URI '%s'. Connecting... " % uri
    s = xmlrpclib.ServerProxy(uri)
    
    print "Calling greet: ", s.greet()

    print 'Done, exiting now.'      


if __name__ == '__main__':
    main()


