#!/bin/sh
./cycleweb.py &
while true;
do
../bitcoin-price-api/scripts/dumpprices.py > prices.csv
mv prices.csv ./cycleweb-react/build/static/prices.csv
./cycledetect.py --dir ./cycleweb-react/build/static arb-all.csv > arb-all.txt
mv arb-all.txt ./cycleweb-react/build/static/arb-all.txt
./cycledetect.py --dir ./cycleweb-react/build/static arb-hk.csv > arb-hk.txt
mv arb-hk.txt ./cycleweb-react/build/static/arb-hk.txt
sleep 15
done

