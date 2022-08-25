#!/bin/bash

while sleep 1 ; do 
    find ./datos -name 'insurance.csv' -o -name 'analisis.py' | entr ./sync.sh 
done