#!/bin/bash
source /home/zzr/RLFuzz_peach/peach-master/venv/bin/activate venv
python2 /home/zzr/RLFuzz_peach/peach-master/sample_analyse.py $1 $2 $3
deactivate
