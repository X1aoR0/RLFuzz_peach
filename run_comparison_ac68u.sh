#!/bin/bash
cd /home/real/Rlfuzz-peach/

methods=("random" "ddpg" "dqn" "double-dqn" "duel-dqn")
# methods=("random" "ddpg")
# envs=("FuzzMd5sum-v0" "FuzzUniq-v0" "FuzzWho-v0" "FuzzBase64-v0")
# envs=("FuzzMd5sum-v0" "FuzzUniq-v0" "FuzzWho-v0" "FuzzBase64-v0")
envs=("FuzzAC68U-v0")

st=`date +%Y-%m-%d_%H:%m:%s`

for env in ${envs[@]}
do
  for method in ${methods[@]}
  do
#   python comparison.py -e $env -m $method -us
    python3 ./rlfuzz/envs/restart_remote_monitor.py -m ssh -u admin -P 608608 -I 192.168.50.1 -p 22 -s "./monitor_ac68u"
    python3 comparison.py -e $env -m $method -st $st -us
  done
done
