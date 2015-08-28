#!/bin/sh

for p in `cat ${1}`; do 
    echo ${p}
    python registre/graph.py -r ${2}/${p}-activities.txt -o ${3}/${p}-graph.pdf -n
done
