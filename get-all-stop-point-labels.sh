#!/bin/bash
OUTPUT=all_stop_points_data.json
touch $OUTPUT

for i in {1..254}; 
do 
echo $i; 
    curl "https://api.navitia.io/v1/coverage/sncf/stop_points?start_page=$i" -H 'Authorization: d3da8e8f-6a39-4e98-833b-719ddabd23a0' | jq >> $OUTPUT
done
