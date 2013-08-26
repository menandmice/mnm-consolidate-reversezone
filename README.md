mnm-consolidate-reversezone
===========================

mnm-consolidate-reversezone is a script to consolidate reverse PTR records from a reverse zone into the parent reverse zone.

For example it can be used to move all PTR records from 10.168.192.in-addr.arpa.,
12.168.192.in-addr.arpa. and 19.168.192.in-addr.arpa. into the zone
168.192.in-addr.arpa.

This script requires the Men & Mice Suite CLI mmcmd ( http://menandmice.com ) binary.

Before the first run, adjust the global variables at the beginning of the script:

```
server   = "<ip-or-hostname-of-Men-and-Mice-Central>"
mmcmdpgm = "/path/to/mmcmd"
user     = "<username-with-enough-access-rights>"
password = "<password>"
masterserver = "<hostname-of-the-primary-master-for-the-new-zone>"
```


```
Usage: mnm-consolidate-reversezone.py [--help | options] target-zone

Options:
  -h, --help  show this help message and exit
  -d          print debug information
  -r          remove migrated PTR records and reverse zones
```

Don't forget the trailing dot "." for the target-zone!
 
Example run:

```
[cas@cstabletx60 ~]$ ./mnm-consolidate-reversezone.py -r  168.192.in-addr.arpa.
Consolidating for reverse zone 168.192.in-addr.arpa.
Creating reverse zone [168.192.in-addr.arpa.]
In zone [1.168.192.in-addr.arpa.]
found PTR record [39.1.168.192.in-addr.arpa.  IN PTR ns1.example.com.]
found PTR record [39.1.168.192.in-addr.arpa.  IN PTR www.example.com.]
removing zone [1.168.192.in-addr.arpa.]
In zone [14.168.192.in-addr.arpa.]
found PTR record [111.14.168.192.in-addr.arpa.  IN PTR new.example.com.]
removing zone [14.168.192.in-addr.arpa.]
In zone [7.168.192.in-addr.arpa.]
found PTR record [11.7.168.192.in-addr.arpa.  IN PTR test.example.com.]
removing zone [7.168.192.in-addr.arpa.]
In zone [88.168.192.in-addr.arpa.]
found PTR record [1.88.168.192.in-addr.arpa.  IN PTR auchnoch.example.com.]
removing zone [88.168.192.in-addr.arpa.]
In zone [168.192.in-addr.arpa.]
add PTR record [39.1.168.192.in-addr.arpa.  IN PTR ns1.example.com.] to zone 168.192.in-addr.arpa.
add PTR record [39.1.168.192.in-addr.arpa.  IN PTR www.example.com.] to zone 168.192.in-addr.arpa.
add PTR record [111.14.168.192.in-addr.arpa.  IN PTR new.example.com.] to zone 168.192.in-addr.arpa.
add PTR record [11.7.168.192.in-addr.arpa.  IN PTR test.example.com.] to zone 168.192.in-addr.arpa.
add PTR record [1.88.168.192.in-addr.arpa.  IN PTR auchnoch.example.com.] to zone 168.192.in-addr.arpa.
```

