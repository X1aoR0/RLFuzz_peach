import rlfuzz
import gym
import os
import time
import numpy as np

ENV_NAME = 'FUzzSocket-v0'
env = gym.make(ENV_NAME)
env.seed(5)  # 起点相同
# nb_actions = env.action_space.shape[0]
nb_actions = env.action_space['mutate'].n
nb_observation = env.observation_space.shape[0]
use_seed = 1

if use_seed:  # 输入初始数据
    data = "abcdaaaaaaaaaaa123456789".encode('utf-8')
    env.set_seed(data)
    print('[+] Use seed, length {}'.format(len(data)))

nb_steps = []

start = time.time()
for s in range(20000):
    if s % 10000 == 0:
        print('[+] {} steps...'.format(s))
    state, reward, done, _ = env.step(env.action_space.sample())
    if done:
        nb_steps.append(s)
end = time.time()

print('[+] {}s'.format(end - start))
history = {}
history['nb_steps'] = nb_steps
