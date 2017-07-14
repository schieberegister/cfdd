#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ###########################################
# SCRIPTNAME: get_ip_v4.py                  #
# AUTHOR:     Benjamin Hofmann              #
# PURPOSE:    Get the WAN-Addresses Adresses#
#             of your Router                #
# DATE:       15.06.2017                    #
# CHANGED:    not yet                       #
#############################################
from urllib2 import urlopen
import socket
from SOAPpy import SOAPProxy
import ipaddress


def validate_ipv4(self, address):

    try:
        ipaddress.IPv4Address(unicode(address))
    except:
        raise
    else:
        return address


def validate_ipv6(self, address):

    try:
        ipaddress.IPv6Address(unicode(address))
    except:
        raise
    else:
        return address


class default:


    def getipv4(self):

        address = urlopen('http://ip.42.pl/raw').read()
        return validate_ipv4(self, address)


    def getipv6(self):

        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        address = s.getsockname()[0]
        return validate_ipv6(self, address)


class fritzbox:
    def getipv4(self):
        url = 'http://fritz.box:49000/igdupnp/control/WANIPConn1'
        namespace = 'urn:schemas-upnp-org:service:WANIPConnection:1'
        address = SOAPProxy(proxy=url,
                            namespace=namespace,
                            soapaction=namespace+'#GetExternalIPAddress',
                            noroot=True).GetExternalIPAddress()
        return validate_ipv4(self, address)

    def getipv6(self):
        d = default()
        return d.getipv6()
