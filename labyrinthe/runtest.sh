#!/bin/sh
python game.py < fifo | python simulator.py mapfile 3 6 23 | tee fifo
