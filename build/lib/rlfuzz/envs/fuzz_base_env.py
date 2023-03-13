import time

import gym
from gym import spaces
import datetime
import copy
import os
import numpy as np
import xxhash
import random
from configparser import ConfigParser

import rlfuzz.coverage as coverage
from rlfuzz.coverage import PATH_MAP_SIZE
from rlfuzz.coverage import MAP_SIZE_SOCKET
from rlfuzz.envs.fuzz_mutator import *
from rlfuzz.envs.sample_analyse import *


class FuzzBaseEnv(gym.Env):
    def __init__(self, socket_flag=False):
        self.socket_flag = False
        self.PeachFlag = False
        # Classes that inherit FuzzBase must define before calling this
        if socket_flag:
            self.engine = coverage.SocketComm(self.target_ip, self.target_port, self.comm_method)
        else:
            self.engine = coverage.Afl(self._target_path, args=self._args, suffix=self._suffix)
        with open("fuzz_cov.txt","w+") as fp:
            fp.write("Begin to record\n")
        self.beginTime = time.time()
        self.recordIter = 0
        self.mutate_num_history = None
        self.muteble_num_list = None
        self.muteble_num = None
        self.seed_block = None
        self.seed_block_list = None
        self.useful_sample_crack_info = None

        self.input_maxsize = self._input_maxsize  # 最大input大小
        self.mutator = FuzzMutatorPlus(self.input_maxsize)  # 变异策略
        self.mutate_size = self.mutator.methodNum  # 变异策略种类
        self.density_size = 256  # [0, 255] 强度定义

        self.initial_seed = True
        self.seed_index = 0  # index of seed in seed list
        self.change_seed_count = 0  # 记录更改种子需要的代数
        self.input_dict = {}  # 记录变异过程中改变覆盖率的样本
        self.multi_seed_input_dict = {}  # 记录多种子变异过程中的改变覆盖率的样本
        self.covHash = xxhash.xxh64()  # 记录覆盖信息的hash

        self.observation_space = spaces.Box(0, 255, shape=(self.input_maxsize,), dtype='uint8')  # 状态空间

        # 1.
        # self.action_space = spaces.Discrete(self.mutate_size)

        # 2.
        # self.action_space = spaces.Box(low=-1, high=1, shape=(3,))  # Mutate,Loc,density

        # 3.
        # self.action_space = spaces.Dict({
        #     'mutate' : spaces.Discrete(self.mutate_size),
        #     'loc_density' : spaces.Box(low=-1, high=1, shape=(2,))
        # })

        # 4.全离散环境
        # 将loc信息分解为4部分 0xffff -> 0xf * 4
        # 将density分解为2部分 0xff -> 0xf * 2
        self.action_space = spaces.Dict({
            'mutate': spaces.Discrete(self.mutate_size),
            'loc': spaces.Tuple((
                spaces.Discrete(16),
                spaces.Discrete(16),
                spaces.Discrete(16),
                spaces.Discrete(16)
            )),
            'density': spaces.Tuple((
                spaces.Discrete(16),
                spaces.Discrete(16)
            ))
        })

        self.isDiscreteEnv = False  # 默认为连续环境

        self.last_input_data = b''  # 记录上一次生成的input
        self.input_len_history = []  # 记录生成input的长度
        self.mutate_history = []  # 记录每次选择的变异策略
        self.reward_history = []  # 记录训练全过程每一步的reward
        self.unique_path_history = []  # 记录发现的新路径数量（coverage_data不同）
        self.transition_count = []  # 记录每次input运行的EDGE数量
        # self.action_history = [] # 记录每次model计算的原始action值
        self.virgin_count = []  # 记录edge访问数量的变化情况

        # 记录全局的edge访问
        if self.socket_flag:
            self.virgin_map = np.array([255] * MAP_SIZE_SOCKET, dtype=np.uint8)
        else:
            self.virgin_map = np.array([255] * PATH_MAP_SIZE, dtype=np.uint8)

        # 记录全局至少访问过一次的edge数量
        self.virgin_single_count = 0

        # 记录全局访问过的新edge的数量（每条edge触发的不同次数视作不同edge）
        self.virgin_multi_count = 0

        # 从配置文件读取保存poc的地址
        self.POC_PATH = r'/tmp'
        cfg = ConfigParser()
        if cfg.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')):
            self.POC_PATH = cfg.get('PATH', 'POC_PATH')

        self.reset()

    # 切换到Discrete环境
    def setDiscreteEnv(self):
        if not self.isDiscreteEnv:
            self.isDiscreteEnv = True
            self.mutator = FuzzMutator(self.input_maxsize)
            self.action_space = spaces.Discrete(self.mutate_size)

    # 恢复默认环境
    def recoverEnv(self):
        if self.isDiscreteEnv:
            self.isDiscreteEnv = False
            self.mutator = FuzzMutatorPlus(self.input_maxsize)
        if not self.PeachFlag:
            self.action_space = spaces.Dict({
                'mutate': spaces.Discrete(self.mutate_size),
                'loc': spaces.Tuple((
                    spaces.Discrete(16),
                    spaces.Discrete(16),
                    spaces.Discrete(16),
                    spaces.Discrete(16)
                )),
                'density': spaces.Tuple((
                    spaces.Discrete(16),
                    spaces.Discrete(16)
                ))
            })
        else:
            self.action_space = spaces.Dict({
                'mutate': spaces.Discrete(self.mutate_size),
                'loc': spaces.Tuple((
                    spaces.Discrete(16),
                    spaces.Discrete(16),
                    spaces.Discrete(16),
                    spaces.Discrete(16)
                )),
                'density': spaces.Tuple((
                    spaces.Discrete(16),
                    spaces.Discrete(16)
                )),
                'block_num': spaces.Discrete(len(self.muteble_num))
            })

    def reset(self):
        self.seed_index = 0
        self.last_input_data = self._seed[self.seed_index]
        self.input_dict = {}
        self.multi_seed_input_dict = {self.seed_index: self.input_dict}

        if self.socket_flag:
            self.virgin_map = np.array([255] * MAP_SIZE_SOCKET, dtype=np.uint8)
        else:
            self.virgin_map = np.array([255] * PATH_MAP_SIZE, dtype=np.uint8)
        self.virgin_single_count = 0
        self.virgin_multi_count = 0

        # 重置其它初始化信息
        self.input_maxsize = self._input_maxsize  # 最大input大小
        if not self.isDiscreteEnv:
            self.mutator = FuzzMutatorPlus(self.input_maxsize)  # 变异策略
        else:
            self.mutator = FuzzMutator(self.input_maxsize)
        self.observation_space = spaces.Box(0, 255, shape=(self.input_maxsize,), dtype='int8')  # 更新状态空间（set_seed后需要修改）

        # 清空记录
        self.input_len_history = []  # 记录生成input的长度
        self.mutate_history = []  # 记录每次选择的变异策略
        self.reward_history = []  # 记录训练全过程每一步的reward
        self.unique_path_history = []  # 记录发现的新路径数量（coverage_data不同）
        self.transition_count = []  # 记录每次input运行的EDGE数量
        self.virgin_count = []
        if self.PeachFlag:
            self.mutate_num_history = []  # 记录每次选择的变异块
            self.useful_sample_crack_info = {}

        assert len(self.last_input_data) <= self.input_maxsize
        return list(self.last_input_data) + [0] * (self.input_maxsize - len(self.last_input_data))

    def actor2actual(self, output, scale):
        return int(output * np.ceil(scale / 2) + np.ceil(scale / 2)) % scale

    # 每个位置被触发1、2、4、8、16、32、64、128次后该处记录归零，不再接受新纪录
    def updateVirginMap(self, covData):
        res = False
        if self.socket_flag:
            RANGE = len(covData)
        else:
            RANGE = PATH_MAP_SIZE
        for i in range(RANGE):
            if covData[i] and covData[i] & self.virgin_map[i]:  # 该位置是否被触发固定次数
                if self.virgin_map[i] == 255:
                    self.virgin_single_count += 1  # 该位置首次被触发
                res = True
                self.virgin_map[i] &= ~(covData[i])
                self.virgin_multi_count += 1  # 该位置被触发（最多记录8次）
        return res

    def step_raw(self, action):

        if not self.isDiscreteEnv:  # 连续环境
            # self.action_history.append(action)
            # action[-2:] = np.clip(action[-2:], -1, 1) # noise可能会使tanh的输出超出[-1,1]
            # assert self.action_space.contains(action), '{}'.format(action)

            # 模型输出 -> actual
            # mutate = self.actor2actual(action[0], self.mutate_size)
            if self.PeachFlag:
                if self.action_space.contains(action):
                    mutate = action['mutate']
                    locs = action['loc']
                    dens = action['density']
                    muteble_block_num = action['block_num']
                else:
                    mutate = np.argmax(action[:self.mutate_size])
                    locs = [np.argmax(action[start: start + 16]) for start in
                            range(self.mutate_size, self.mutate_size + 64, 16)]
                    dens = [np.argmax(action[start: start + 16]) for start in
                            range(self.mutate_size + 64, self.mutate_size + 64 + 32, 16)]
                    muteble_block_num = np.argmax(action[self.mutate_size + 64 + 32:])
                ll = [12, 8, 4, 0]
                loc = sum([n << l for n, l in zip(locs, ll)])
                density = sum([n << l for n, l in zip(dens, ll[-2:])])
                # 根据可变异块的编号选择变异位置
                mutate_block_index = self.muteble_num[muteble_block_num]
                (block_start_loc, block_length) = self.seed_block[mutate_block_index]
                if self.initial_seed:
                    input_data = self.last_input_data
                else:
                    # 选择变异策略对last_input_data进行变异操作
                    tmp_input_data_front = self.last_input_data[:block_start_loc]
                    block_input_data = self.last_input_data[block_start_loc:block_start_loc + block_length]
                    tmp_input_data_behind = self.last_input_data[block_start_loc + block_length:]
                    new_block_data = self.mutator.mutate(mutate, block_input_data, loc, density)
                    new_block_length = len(new_block_data)
                    self.seed_block[mutate_block_index][1] = new_block_length
                    for i in range(mutate_block_index + 1, len(self.seed_block)):
                        self.seed_block[i][0] += new_block_length - block_length

                    input_data = tmp_input_data_front + new_block_data + tmp_input_data_behind

            else:
                if self.action_space.contains(action):
                    mutate = action['mutate']
                    locs = action['loc']
                    dens = action['density']
                else:
                    mutate = np.argmax(action[:self.mutate_size])
                    locs = [np.argmax(action[start: start + 16]) for start in
                            range(self.mutate_size, self.mutate_size + 64, 16)]
                    dens = [np.argmax(action[start: start + 16]) for start in
                            range(self.mutate_size + 64, self.mutate_size + 64 + 32, 16)]
                ll = [12, 8, 4, 0]
                loc = sum([n << l for n, l in zip(locs, ll)])
                density = sum([n << l for n, l in zip(dens, ll[-2:])])
                if self.initial_seed:
                    input_data = self.last_input_data
                else:
                    input_data = self.mutator.mutate(mutate, self.last_input_data, loc, density)
        else:  # 离散环境
            if self.action_space.contains(action):
                mutate = action
            else:
                mutate = np.argmax(action)
            assert self.action_space.contains(mutate)
            input_data = self.mutator.mutate(mutate, self.last_input_data)

        # 记录动作历史
        self.mutate_history.append(mutate)

        # 记录每一步产生的input字符长度
        self.input_len_history.append(len(input_data))

        # 记录每次选择的变异块
        if self.PeachFlag:
            self.mutate_num_history.append(mutate_block_index)

        # 执行一步获取覆盖率信息
        self.coverageInfo = self.engine.run(input_data)
        self.initial_seed = False
        # 记录产生新覆盖记录的input
        self.covHash.reset()
        self.covHash.update(self.coverageInfo.coverage_data.tostring())
        tmpHash = self.covHash.digest()
        # if tmpHash not in list(self.input_dict): # 如果当前变异产生新覆盖则选择变异后样本进行下一次变异
        if self.updateVirginMap(self.coverageInfo.coverage_data):
            reward = self.coverageInfo.reward()
            self.change_seed_count = 0  # 更换种子计数清零
            self.input_dict[tmpHash] = input_data
            self.last_input_data = input_data
            if self.PeachFlag:
                self.useful_sample_crack_info[tmpHash] = [self.seed_block, self.muteble_num]
        else:  # 从记录中随机选择待变异样本
            self.change_seed_count += 1
            reward = self.coverageInfo.reward()
            if not self.input_dict:  # 如果当前种子没有产生过有用的样本
                self.Change_Seed()  # 更换一个初始种子
            else:
                rand_choice = random.choice(list(self.input_dict))
                self.last_input_data = self.input_dict[rand_choice]
                if self.PeachFlag:  # update model crack result when not fuzz in sequence
                    self.seed_block, self.muteble_num = copy.deepcopy(self.useful_sample_crack_info[rand_choice][0]), \
                                                        self.useful_sample_crack_info[rand_choice][1]

        self.virgin_count.append([self.virgin_single_count, self.virgin_multi_count])  #
        self.unique_path_history.append(
            sum([len(value) for value in self.multi_seed_input_dict.values()]))  # 记录每一步之后发现的总的有效样本数

        # 记录每一步运行的EDGE数量
        self.transition_count.append(self.coverageInfo.transition_count())
        if self.change_seed_count >= 100:
            self.Change_Seed()  # 连续100个种子未产生新的路径，就切换种子
        return {
            "reward": min(1, reward),
            "input_data": input_data,
            "crash_info": True if self.coverageInfo.crashes > 0 else False  # 是否发生崩溃
        }

    def step(self, action):

        info = self.step_raw(action)
        reward = info['reward']
        assert reward <= 1

        if info['crash_info']:
            # reward = 1 # 调整奖励
            done = True
            name = '{}-{}'.format(os.path.basename(self._target_path),
                                  datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f'))  # 精确到微秒防止冲突
            print(' [+] Find {}'.format(name))
            with open(os.path.join(self.POC_PATH, name), 'wb') as fp:
                fp.write(info['input_data'])
        else:
            done = False
        curTime = time.time()
        if curTime-self.beginTime > self.recordIter*3600:
            self.recordIter  = self.recordIter+1
            with open("fuzz_cov.txt", "w+") as fp:
                fp.write("recordIter{} : cov is {}\n".format(self.recordIter,reward))
        # 记录reward
        self.reward_history.append(reward)

        # 将input_data转化为用于NN的state格式
        state = [m for m in info['input_data']]
        trail = [0] * (self.input_maxsize - len(state))
        state += trail

        assert len(state) == self.input_maxsize, '[!] len(state)={}, self.input_maxsize={}'.format(len(state),
                                                                                                   self.input_maxsize)

        return state, reward, done, {}

    def render(self, mode='human', close=False):
        pass

    def eof(self):
        return self._dict.eof()

    def dict_size(self):
        return self._dict.size()

    def input_size(self):
        return self.input_maxsize

    def get_poc_path(self):
        return self.POC_PATH

    def Change_Seed(self):
        self.change_seed_count = 0
        seed_length = len(self._seed)
        if seed_length == 1:  # 只有一个种子直接返回
            return
        self.seed_index += 1  # 选择下一个种子
        self.seed_index %= seed_length  # 防止越界
        self.observation_space = spaces.Box(0, 255, shape=(self.input_maxsize,),
                                            dtype='int8')  # 更新状态空间（set_seed后需要修改）

        if self.seed_index in self.multi_seed_input_dict:
            self.input_dict = self.multi_seed_input_dict[self.seed_index]
            while not self.input_dict:
                self.seed_index += 1  # 选择下一个种子
                self.seed_index %= seed_length  # 防止越界
                if self.seed_index in self.multi_seed_input_dict:
                    self.input_dict = self.multi_seed_input_dict[self.seed_index]
                else:
                    self.input_dict = {}
                    self.multi_seed_input_dict[self.seed_index] = self.input_dict
                    self.initial_seed = True
                    break
        else:
            self.input_dict = {}
            self.multi_seed_input_dict[self.seed_index] = self.input_dict
            self.initial_seed = True
        self.last_input_data = self._seed[self.seed_index]
        if self.PeachFlag:
            self.recoverEnv()  # 重设环境修改num_block的大小
            self.seed_block = copy.deepcopy(self.seed_block_list[self.seed_index])
            self.muteble_num = self.muteble_num_list[self.seed_index]

    def set_peach(self):
        self.PeachFlag = True
        # 记录当前样本的格式约束解析结果 (位置，长度)  记录可变异的块的序号
        # self.seed_block, self.muteble_num = Sample_dataCrack(self._dataModelName,
        #                                                      self._Seed_Path,
        #                                                      self._PitPath)
        if os.path.isfile(self._Seed_Path):
            self.seed_block, self.muteble_num = NewSample_dataCrack(self._dataModelName,
                                                                    self._Seed_Path,
                                                                    self._PitPath)
        elif os.path.isdir(self._Seed_Path):
            self.seed_block_list = []
            self.muteble_num_list = []
            for each in self.seed_names:
                if each.endswith(self._suffix):
                    tmp_seed_block, tmp_muteble_num = NewSample_dataCrack(self._dataModelName,
                                                                          os.path.join(self._Seed_Path, each),
                                                                          self._PitPath)
                    self.seed_block_list.append(tmp_seed_block)
                    self.muteble_num_list.append(tmp_muteble_num)
            self.seed_block = copy.deepcopy(self.seed_block_list[self.seed_index])
            self.muteble_num = self.muteble_num_list[self.seed_index]
        self.mutate_num_history = []  # 记录每次选择的变异块
        self.useful_sample_crack_info = {}
        # 5. 加入格式约束
        self.action_space = spaces.Dict({
            'mutate': spaces.Discrete(self.mutate_size),
            'loc': spaces.Tuple((
                spaces.Discrete(16),
                spaces.Discrete(16),
                spaces.Discrete(16),
                spaces.Discrete(16)
            )),
            'density': spaces.Tuple((
                spaces.Discrete(16),
                spaces.Discrete(16)
            )),
            'block_num': spaces.Discrete(len(self.muteble_num))
        })
        self.reset()
