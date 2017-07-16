#!/bin/bash 

REMOTEHOST="192.168.1.8"
BASE="/opt/pirest-sense-hat/"

for i in $(git ls-tree -r master --name-only); do
    echo $i; 
    scp ${i} root@${REMOTEHOST}:${BASE}/$i
done

# Ficheros aún sin control de versiones
for i in "apirest/utils.py"; do
    echo $i;
    scp ${i} root@${REMOTEHOST}:${BASE}/$i
done

