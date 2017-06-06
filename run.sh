#!/bin/sh
while true;
do
../bitcoin-price-api/scripts/dumpprices.py > ./cycleweb-react/build/static/prices.csv
./cycledetect.py  ./cycleweb-react/build/static/*.csv > ./cycleweb-react/build/static/arb.txt
sleep 15
done
 
