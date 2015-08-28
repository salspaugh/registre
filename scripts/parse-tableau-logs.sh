#!/bin/sh

for p in `cat ${1}`; do 
    echo ${p}
    python registre/map.py -i ${2}/${p}-log.txt -o ${3}/${p}-activities.txt
done
