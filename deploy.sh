#!/bin/bash 

REMOTEHOST="192.168.1.8"
BASE="/opt/pirest-sense-hat/"

for i in "apirest pirest-sense-hat"; do
    scp -r ${i} root@${REMOTEHOST}:${BASE}
done