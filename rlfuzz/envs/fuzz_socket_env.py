from rlfuzz.envs.fuzz_base_env import FuzzBaseEnv


class FuzzSocketEnv(FuzzBaseEnv):
    def __init__(self):
        self.target_ip = '192.168.50.1'
        self.target_port = 80
        self._seed = b''  # 指定初始变异的文件
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小

        super(FuzzSocketEnv, self).__init__(socket_flag=True)

    def set_seed(self, seed):
        assert len(seed) > 0
        assert isinstance(seed, bytes)
        self._seed = seed
        self._input_maxsize = len(seed)
        self.reset()


class FuzzAC68UEnv(FuzzBaseEnv):
    def __init__(self):
        self.target_ip = '192.168.108.128'
        self.target_port = 80
        self._seed = b''  # 指定初始变异的文件
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self.comm_method = 'TCP'
        self._target_path = '/AC68U'
        self.PeachFlag = True
        if self.PeachFlag:
            self._Seed_Path = '/home/real/Rlfuzz-peach/rlfuzz/test/sample/4.txt'
            self._dataModelName = 'HttpRequest'
            self._PitPath = 'file:test/pit/web_datamodel.xml'

        super(FuzzAC68UEnv, self).__init__(socket_flag=True, PeachFlag=self.PeachFlag)

    def set_seed(self, seed):
        assert len(seed) > 0
        assert isinstance(seed, bytes)
        self._seed = seed
        # self._input_maxsize = len(seed)
        self.reset()


class FuzzAC9Env(FuzzBaseEnv):
    def __init__(self):
        self.target_ip = '192.168.0.1'
        self.target_port = 80
        self._seed = b''  # 指定初始变异的文件
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self.comm_method = 'UDP'

        super(FuzzAC9Env, self).__init__(socket_flag=True)

    def set_seed(self, seed):
        assert len(seed) > 0
        assert isinstance(seed, bytes)
        self._seed = seed
        self._input_maxsize = len(seed)
        self.reset()
