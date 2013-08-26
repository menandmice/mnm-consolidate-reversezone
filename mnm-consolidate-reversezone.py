#!/usr/bin/env python3
# Copyright (C) 2013 Men & Mice
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND MEN & MICE DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL MEN & MICE BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

"""
mnm-consolidate-reversezone is a script to consolidate reverse PTR
records from a reverse zone into the parent reverse zone. For example
it can be used to move all PTR records from 10.168.192.in-addr.arpa.,
12.168.192.in-addr.arpa. and 19.168.192.in-addr.arpa. into the zone
168.192.in-addr.arpa.

This script requires the Men & Mice Suite CLI mmcmd

Author: Carsten Strotmann - carsten@menandmice.com
Version: 0.2
Date: 2013-08-26
"""

import os
import sys
import subprocess
import string
from optparse import OptionParser

server   = "127.0.0.1"
mmcmdpgm = "/usr/bin/mmcmd"
user     = "administrator"
password = "menandmice"
masterserver = "ns1.example.com"

def mmcmd(cmd, debugflag=False):
    if debugflag: 
        print("mmcmd {}".format(cmd))
    output = subprocess.check_output([mmcmdpgm, 
                                      "-q", "-s{}".format(server), 
                                      "-u{}".format(user), 
                                      "-p{}".format(password), 
                                      "{}; quit;".format(cmd)], timeout=60).decode("utf8")
    return output


# Main program
if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [--help | options] target-zone")
    parser.add_option("-d", action="store_true", dest="debugflag",
                      default=False, help="print debug information")
    parser.add_option("-r", action="store_true", dest="removeflag",
                      default=False, 
                      help="remove migrated PTR records and reverse zones")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("you must supply the name of the target zone")

    revzone  = args[0].lower()

    print ("Consolidating for reverse zone {}".format(revzone))

    zones = mmcmd("zones", options.debugflag)
    zones = zones.splitlines()
    zonelist = [z.split(" ",1)[0] for z in zones]
    zonelist = [z for z in zonelist if z.endswith(revzone)]    
    if options.debugflag:
        print("Zonelist: {}".format(zonelist)) 

    if not revzone in zonelist:
        print ("Creating reverse zone [{}]".format(revzone))
        output = mmcmd("addzone {} {} *; save {}".format(revzone,
                                                         masterserver,
                                                         revzone ),
                       options.debugflag)
    else:
        zonelist.remove(revzone)
    
    ptrs = []
    for z in zonelist:
        print("In zone [{}]".format(z))
        records = mmcmd("print {}".format(z))
        records = records.splitlines()
        records = [r.split("\t",4) for r in records]

        for r in records:
            owner, ttl, netclass, rtype, rdata  = r[0], r[1], r[2], r[3], r[4]
            if rtype == "PTR":
                owner = "{}.{}".format(owner, z)
                record = " ".join([owner,ttl,netclass,rtype, rdata])
                ptrs.append(record)
                print("found PTR record [{}]".format(record))
        if options.removeflag:
            print("removing zone [{}]".format(z))
            rc = mmcmd("deletezone {}".format(z))
    print("In zone [{}]".format(revzone))
    for p in ptrs:
        print("add PTR record [{}] to zone {}".format(p, revzone))
        rc = mmcmd("add {} -1 {}; save {}".format(revzone, p, revzone),options.debugflag)
    
