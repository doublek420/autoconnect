"""
Project setuptools config...

(c) Oisin Mulvihill
2007-07-10

"""
from setuptools import setup, find_packages

Name='autoconnect'
ProjecUrl="" #"http://www.sourceweaver.com/autoconnect"
Version='0.9.3'
Author='Oisin Mulvihill'
AuthorEmail='oisin dot mulvihill at gmail com'
Maintainer=' Oisin Mulvihill'
Summary='This utility helps auto negotiate a socket connection between a client and server app.'
License='LGPL'
ShortDescription="This module helps in automatic client-server discovery and connection setup for networked applications."
Description="""This module helps in automatic client-server discovery and connection setup for networked applications.

I wrote this module a while ago (5+ years) and thought it would be handy
for others. Its a handy auto-socket connection module. I used it 
originally in a internet cafe management system. The client app installed
on the PC would start the receiver. It would then wait for the server 
to broadcast its URL and on receiving it connect and do its business. 

I've recently had call to want to do this type of thing again so I thought
I'd dust this code off and make into a proper project. I'll release the 
code I've got first then improve it as I start using again.

The developer access to the code is available on:

    http://code.google.com/p/autoconnect/


"""

TestSuite = 'autoconnect.tests'

ProjectScripts = [
#    '',
]

PackageData = {
    # If any package contains *.txt or *.rst files, include them:
    '': ['*.txt', '*.rst', 'ini'],
}

setup(
#    url=ProjecUrl,
    name=Name,
    version=Version,
    author=Author,
    author_email=AuthorEmail,
    description=ShortDescription,
    long_description=Description,
    license=License,
    test_suite=TestSuite,
    scripts=ProjectScripts,
    packages=find_packages('lib'),
    package_data=PackageData,
    package_dir = {'': 'lib'},
)
