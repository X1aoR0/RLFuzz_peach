#!/bin/bash
cd /home/bupt1112/data/ai-fuzz/examples

# methods=("random" "ddpg" "dqn" "double-dqn" "duel-dqn")
methods=("random" "ddpg")
# envs=("FuzzMd5sum-v0" "FuzzUniq-v0" "FuzzWho-v0" "FuzzBase64-v0")
envs=("FuzzMd5sum-v0" "FuzzUniq-v0" "FuzzWho-v0" "FuzzBase64-v0")

st=`date +%Y-%m-%d_%H:%m:%s`

for env in ${envs[@]}
do
  for method in ${methods[@]}
  do
#     python comparison.py -e $env -m $method -us
    python3 comparison.py -e $env -m $method -st $st
  done
done
