#!/bin/sh
while true;
do
../bitcoin-price-api/scripts/dumpprices.py > prices.csv
mv prices.csv ./cycleweb-react/build/static/prices.csv
./cycledetect.py  ./cycleweb-react/build/static/transaction.csv \
		  ./cycleweb-react/build/static/prices.csv > arb.txt
mv arb.txt ./cycleweb-react/build/static/arb.txt
sleep 15
done
 
