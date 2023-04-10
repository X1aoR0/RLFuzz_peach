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
from ZZRFuzz.ZZRFuzz_crackseed import *
from ZZRFuzz.ZZRFuzz_computeRate import *
from ZZRFuzz import config
class FuzzBaseEnv(gym.Env):
    def __init__(self, socket_flag=False):
        self.socket_flag = False
        self.PeachFlag = False
        # Classes that inherit FuzzBase must define before calling this
        # 这里选择引擎，正常就是AFL的老引擎  如果是对固件的测试，就用Socket
        if socket_flag:
            self.engine = coverage.SocketComm(self.target_ip, self.target_port, self.comm_method)
        #
        else:
            self.engine = coverage.Afl(self._target_path, args=self._args)

        self.beginTime = time.time()
        with open("fuzz_cov.txt","w+") as fp:
            fp.write("Begin to record " + str(self.beginTime) +"\n")
        self.count = 0
        self.recordIter = 0
        self.mutate_num_history = None
        self.muteble_num_list = None
        self.muteble_num = None #变异块的数量
        self.seed_block = None
        self.seed_block_list = None
        self.useful_sample_crack_info = None

        self.input_maxsize = self._input_maxsize  # 最大input大小
        self.mutator = FuzzMutatorPlus(self.input_maxsize)  # 变异策略
        self.mutate_size = self.mutator.methodNum+1  # 变异策略种类
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
        self.new_step = 0
        self.last_step = 0
        # 从配置文件读取保存poc的地址
        self.POC_PATH = r'/tmp'
        cfg = ConfigParser()
        if cfg.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')):
            self.POC_PATH = cfg.get('PATH', 'POC_PATH')
        self.initial_seed_cmp_map = {}
        self.initial_seed_cov = {}
        self.seed_but_not_initial = False
        self.is_single_byte_mutate = False
        self.key_byte_list = []
        self.key_byte_list.append(0)
        self.reset()
        self.cur_state = 0
    # 切换到Discrete环境
    def setDiscreteEnv(self):
        if not self.isDiscreteEnv:
            self.isDiscreteEnv = True
            self.mutator = FuzzMutator(self.input_maxsize)
            self.action_space = spaces.Discrete(self.mutate_size)

    def reset(self):
        self.seed_index = 0  #reset seed index to 0
        self.last_input_data = self._seed[self.seed_index] #reset input_data to seed[seed_index]
        self.input_dict = {}  #reset interesting seed list
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

        # # 清空记录
        # self.input_len_history = []  # 记录生成input的长度
        # self.mutate_history = []  # 记录每次选择的变异策略
        # self.reward_history = []  # 记录训练全过程每一步的reward
        # self.unique_path_history = []  # 记录发现的新路径数量（coverage_data不同）
        # self.transition_count = []  # 记录每次input运行的EDGE数量
        # self.virgin_count = []
        # if self.PeachFlag:
        #     self.mutate_num_history = []  # 记录每次选择的变异块
        #     self.useful_sample_crack_info = {}

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
        loc = 0
        new_block_length = 0
        block_start_loc = 0
        if not self.isDiscreteEnv:  # 连续环境
            # self.action_history.append(action)
            # action[-2:] = np.clip(action[-2:], -1, 1) # noise可能会使tanh的输出超出[-1,1]
            # assert self.action_space.contains(action), '{}'.format(action)

            # 模型输出 -> actual
            # mutate = self.actor2actual(action[0], self.mutate_size)
            # locs


            if self.PeachFlag:
                if self.action_space.contains(action):
                    mutate = action['mutate']
                    locs = action['loc']
                    dens = action['density']
                    mutable = action['block_num']
                else:
                    mutate = np.argmax(action[:self.mutate_size])
                    locs = [np.argmax(action[start: start + 16]) for start in
                            range(self.mutate_size, self.mutate_size + 64, 16)]
                    dens = [np.argmax(action[start: start + 16]) for start in
                            range(self.mutate_size + 64, self.mutate_size + 64 + 32, 16)]
                    mutable = [np.argmax(action[start: start + 16]) for start in
                               range(self.mutate_size + 64 + 32, self.mutate_size + 64 + 32 + 32,
                                     16)]  # np.argmax(action[self.mutate_size + 64 + 32:])
                # force to single byte mutate
                mutate = mutate%3
                if mutate == 0:
                    mutate = 3
                elif mutate == 1:
                    mutate = 4
                else:
                    mutate = self.mutator.methodNum

                if mutate == 3 or mutate == 4 or mutate == self.mutator.methodNum:
                    self.is_single_byte_mutate = True
                else:
                    self.is_single_byte_mutate = False

                ll = [12, 8, 4, 0]
                #这一步是把locs拼装起来，因为action是把他分成0xf,0xf,0xf,0xf了
                loc = sum([n << l for n, l in zip(locs, ll)])
                #拼装density
                density = sum([n << l for n, l in zip(dens, ll[-2:])])
                #拼装，为啥多除一个256
                muteble_block_num = int(sum([n << l for n, l in zip(mutable, ll[-2:])]) / 256 * len(self.muteble_num))
                # 根据可变异块的编号的下标选择可变异块的编号
                if len(self.muteble_num) == 0:
                    mutate_block_index = 0
                else:
                    mutate_block_index = self.muteble_num[muteble_block_num]
                # 根据下标找到对应的种子块
                (block_start_loc, block_length) = self.seed_block[mutate_block_index]
                if self.initial_seed:
                    input_data = self.last_input_data
                else:
                    # 选择变异策略对last_input_data进行变异操作
                    tmp_input_data_front = self.last_input_data[:block_start_loc]
                    block_input_data = self.last_input_data[block_start_loc:block_start_loc + block_length]
                    tmp_input_data_behind = self.last_input_data[block_start_loc + block_length:]
                    new_block_data = self.mutator.mutate(mutate, block_input_data, loc, density,self.key_byte_list)
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

        if self.initial_seed == True:
            with open("/tmp/cmp_log_config", "w") as cmp_log_config:
                cmp_log_config.write("1")
            config.cmp_log_flag = 1
            # 执行一步获取覆盖率信息
            self.coverageInfo,cmp_map = self.engine.run(input_data)
            self.initial_seed_cmp_map[self.seed_index] = cmp_map
            with open("/tmp/cmp_log_config", "w") as cmp_log_config:
                cmp_log_config.write("0")
            config.cmp_log_flag = 0
        elif self.seed_but_not_initial and self.is_single_byte_mutate and not config.Stage_3:
            self.seed_but_not_initial = False
            self.is_single_byte_mutate = False
            with open("/tmp/cmp_log_config", "w") as cmp_log_config:
                cmp_log_config.write("1")
            config.cmp_log_flag = 1
            # 执行一步获取覆盖率信息
            self.coverageInfo,cmp_map = self.engine.run(input_data)

            with open("/tmp/cmp_log_config", "w") as cmp_log_config:
                cmp_log_config.write("0")
            config.cmp_log_flag = 0
            # cal key byte
            mute_byte_index = block_start_loc + loc % new_block_length
            cur_byte = input_data[mute_byte_index]
            init_byte = self.input_dict[self.initial_seed_cov[self.seed_index]][mute_byte_index]
            cur_ket_byte_list = computeRate(self.initial_seed_cmp_map[self.seed_index],cmp_map,init_byte,cur_byte)

            for x in list(set(cur_ket_byte_list)):
                self.key_byte_list.append(x)

            with open("./key_byte_list", "a+") as key_list_fp:
                key_list_fp.write("iter "+ str(self.count)+": "+str(self.key_byte_list))
        else:
            self.coverageInfo, cmp_map = self.engine.run(input_data)

        # 记录产生新覆盖记录的input
        self.covHash.reset()
        self.covHash.update(self.coverageInfo.coverage_data.tostring())
        tmpHash = self.covHash.digest()
        if self.initial_seed == True:
            self.initial_seed_cov[self.seed_index] = tmpHash
        self.initial_seed = False
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
                if rand_choice == self.initial_seed_cov[self.seed_index]:
                    self.seed_but_not_initial = True

                if self.PeachFlag:  # update model crack result when not fuzz in sequence
                    self.seed_block, self.muteble_num = copy.deepcopy(self.useful_sample_crack_info[rand_choice][0]), \
                                                        self.useful_sample_crack_info[rand_choice][1]

        self.virgin_count.append([self.virgin_single_count, self.virgin_multi_count])  #
        self.unique_path_history.append(
            sum([len(value) for value in self.multi_seed_input_dict.values()]))  # 记录每一步之后发现的总的有效样本数

        # print edge info
        with open("/home/zzr/RLFuzz_peach/edgerate.txt", 'a+') as fp:
            #fp.write(info['input_data'])
            fp.write("current edge rate:"+str(self.coverageInfo.transition_count() / 65535) + "\n")
            fp.write("total edge num:" + str(self.virgin_single_count /65535) + "\n")
        print("\n"+"current edge rate:"+str(self.coverageInfo.transition_count() / 65535) + "\n")
        print("\n"+"total edge num:" + str(self.virgin_single_count) + "\n")
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
        self.new_step = time.perf_counter()
        elapsed_time = (self.new_step - self.last_step) * 1000
        print(f"new step cost : {elapsed_time:.3f} ms")


        self.count = self.count+1
        start_step_raw_time = time.perf_counter()
        info = self.step_raw(action)
        end_step_raw_time = time.perf_counter()
        elapsed_time = (end_step_raw_time - start_step_raw_time) * 1000

        print(f"step_raw cost : {elapsed_time:.3f} ms")
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
        if curTime-self.beginTime > self.recordIter*1800:
            self.recordIter  = self.recordIter+1
            with open("fuzz_cov.txt", "a+") as fp:
                fp.write("recordIter{} : cov is {} ; edge num is {} ; mutenum is {}\n".format(self.recordIter,reward,self.virgin_single_count,self.count))
        # 记录reward
        self.reward_history.append(reward)

        # 将input_data转化为用于NN的state格式
        state = [m for m in info['input_data']]
        trail = [0] * (self.input_maxsize - len(state))
        state += trail

        assert len(state) == self.input_maxsize, '[!] len(state)={}, self.input_maxsize={}'.format(len(state),
                                                                                                   self.input_maxsize)
        self.last_step = time.perf_counter()
        self.cur_state = state
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
        #if this seed already mutated
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
            self.seed_block = copy.deepcopy(self.seed_block_list[self.seed_index])
            self.muteble_num = self.muteble_num_list[self.seed_index]

    def set_peach_new(self):
        self.PeachFlag = True
        # 记录当前样本的格式约束解析结果 (位置，长度)  记录可变异的块的序号
        # self.seed_block, self.muteble_num = Sample_dataCrack(self._dataModelName,
        #                                                      self._Seed_Path,
        #                                                      self._PitPath)
        # 如果Seed_path是文件，就直接保存一个seed_block和mutable_num
        if os.path.isfile(self._Seed_Path):
            self.seed_block, self.muteble_num = seedCrack(self.engine,self._Seed_Path)
        # 如果Seed_path是目录，就crack之后添加到list里面
        elif os.path.isdir(self._Seed_Path):
            self.seed_block_list = []
            self.muteble_num_list = []
            for each in self.seed_names:
                if each.endswith(self._suffix):
                    tmp_seed_block, tmp_muteble_num = seedCrack(self.engine,os.path.join(self._Seed_Path, each))
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
            'block_num': spaces.Tuple((
                spaces.Discrete(16),
                spaces.Discrete(16)
            ))
        })
        self.reset()


    def set_peach(self):
        self.PeachFlag = True
        # 记录当前样本的格式约束解析结果 (位置，长度)  记录可变异的块的序号
        # self.seed_block, self.muteble_num = Sample_dataCrack(self._dataModelName,
        #                                                      self._Seed_Path,
        #                                                      self._PitPath)
        # 如果Seed_path是文件，就直接保存一个seed_block和mutable_num
        if os.path.isfile(self._Seed_Path):
            self.seed_block, self.muteble_num = NewSample_dataCrack(self._dataModelName,
                                                                    self._Seed_Path,
                                                                    self._PitPath)
        # 如果Seed_path是目录，就crack之后添加到list里面
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
            'block_num': spaces.Tuple((
                spaces.Discrete(16),
                spaces.Discrete(16)
            ))
        })
        self.reset()
