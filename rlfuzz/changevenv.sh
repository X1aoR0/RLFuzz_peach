#!/bin/bash
source /home/real/peach-master/venv/bin/activate venv
python2 /home/real/peach-master/sample_analyse.py $1 $2 $3
deactivate
