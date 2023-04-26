#!/usr/bin/env bash
CONSTS_PATHS=( $(find . -type f -name consts.py) )
for ((cont=0; cont<${#CONSTS_PATHS[@]}; cont++)) do 
       cp --force --verbose consts/consts.py ${CONSTS_PATHS[$cont]}
done
