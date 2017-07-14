#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ##########################################
# SCRIPTNAME: cfdnsupd.py v 0.9            #
# AUTHOR:     Benjamin Hofmann             #
# PURPOSE:    Update CloudFlare DNS entrys #
#             from the destination host    #
# DATE:       14.02.2017                   #
# CHANGED:    not yet                      #
############################################

import logging
from configparser import ConfigParser
from cf_api import CloudFlare
import get_ip
import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))
logging.FileHandler('update.log')
parser = ConfigParser()
parser.read('cfdd.conf')

try:
    router = getattr(get_ip, parser.get("GENERAL", "router"))()
except:
    logging.error("Could not get your router class. TIP: Use default instead")

try:
    pubipv4addr = router.getipv4()
    if parser.get("GENERAL", "updateipv6") == "yes":
        pubipv6addr = router.getipv6()
except:
    logging.error("Problems obtaining public IP")

cf_email = parser.get("GENERAL", "cf_email")
cf_apiky = parser.get("GENERAL", "cf_apiky")
cf = CloudFlare(cf_email, cf_apiky)
for section_name in parser.sections():
    if section_name != "GENERAL":
        records_conf = parser.get(section_name, 'substoupdate')
        records = records_conf.split('\n')
        for record in records:
            if pubipv4addr != cf.get_record_ip(section_name, record, "A"):
                cf.update_dns_record(section_name, record, "A", pubipv4addr)

            if parser.get("GENERAL", "updateipv6") == 'yes':
                if pubipv6addr != cf.get_record_ip(section_name, record, "AAAA"):
                    cf.update_dns_record(section_name, record, "AAAA", pubipv6addr)
