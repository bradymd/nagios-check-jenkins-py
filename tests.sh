set -x 
./checkjenky.py
sleep 2
./checkjenky.py -h
sleep 2
./checkjenky.py -j "(vcl-la-rwa03) Import notification logs"
sleep 2
./checkjenky.py -j "(hokey cokey"
sleep 2
./checkjenky.py -j "(ask) Staging wayfinding index",
sleep 2
./checkjenky.py -j "(vcl-la-rwa03) Import notification logs" "(hokey cokey)" "(vcl-la-rwa03) Import AWS notification logs",
