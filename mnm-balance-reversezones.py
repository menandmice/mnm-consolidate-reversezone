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
This script balances the forward lookup and reverse lookup zones. It
checks that all A/AAAA record entries have matching PTR records, and
it looks for PTR records without matching A/AAAA records (orphaned PTR
records). 

It is the script version of the "reverse-zone-wizard" and the "find
orphan PTR records" functions in the Men & Mice GUI.

This script requires the Men & Mice Suite CLI mmcmd

Author: Carsten Strotmann - carsten@menandmice.com
Version: 0.1 (wip)
Date: 2013-09-04
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
    parser = OptionParser(usage="Usage: %prog [--help | options]")
    parser.add_option("-d", action="store_true", dest="debugflag",
                      default=False, help="print debug information")
    parser.add_option("-r", action="store_true", dest="removeflag",
                      default=False, 
                      help="remove orphaned PTR records")
    parser.add_option("-a", action="store_true", dest="addflag",
                      default=False, 
                      help="add missing PTR records")
    (options, args) = parser.parse_args()

    print ("Balancing reverse zones ...")

    zones = mmcmd("zones", options.debugflag).lower()
    zones = zones.splitlines()
    zonelist = [z.split(" ",1)[0] for z in zones]
    zonelist = [z for z in zonelist if not '::' in z]
    rev4zonelist = [z for z in zonelist if z.endswith("in-addr.arpa")]    
    rev6zonelist = [z for z in zonelist if z.endswith("ip6.arpa")]    


