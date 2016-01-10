# The Auto Connect Project #

## Introduction ##

This module provides the handy ability to get a connection string from a client to server,
without having to do specific configuration. The basic idea is the server broadcast on a
small list of random ports. The client listens on one of these random ports. When it
receives the broadcast the data contains the connection string for the server.

One example usage is in an internet cafe management system I developed. The client program
was installed via a windows installer. Originally the user then had to edit the config for
each machine in the shop. This was fine for one or two machines. However if you've got 70+
machines this it took a long time to update the configuration. One solution is to have default
set up locations. However if you have to move the server off the default or change it later,
then you need to update all the clients again.

My solution to this was to use UDP broadcasts. The server ran a 'beckon' when the clients
'watched' for. When the client started it watched for the beckon. Upon 'seeing' it, it was
able to connect. The clients stopped watching for the server beckon until it lost its
connection or the server went down. This was very useful and was later expanded to tell
clients about other servers that were near by.


## Example ##

The "autoconnect.example" contains an example client and server that models the basic idea.
The "test\_server.py" runs a simple XML-RPC server and the "test\_client.py" discovers this
and connects to call the greet() method.

The unit test case for this project also illustrate how the project is used. Look in the
"autoconnect.tests" for further details.


