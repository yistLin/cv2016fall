#!/bin/bash

for img in $@ ; do
    ./noise_removal.py --filter=box ${img}
    ./noise_removal.py --filter=median ${img}
    ./noise_removal.py --filter=opening_closing ${img}
    ./noise_removal.py --filter=closing_opening ${img}
done
