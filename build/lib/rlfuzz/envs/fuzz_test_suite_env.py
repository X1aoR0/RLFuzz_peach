import rlfuzz
from rlfuzz.envs.fuzz_base_env import FuzzBaseEnv
import os


class FuzzlibpngEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.libpng_target_path()
        self._args = ['']
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = '.png'
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._dataModelName = 'PNG'
        self._PitPath = 'file:test/pit/png_datamodel.xml'
        super(FuzzlibpngEnv, self).__init__()

    def set_seed(self, seed_path):
        if os.path.isfile(seed_path):
            with open(seed_path, 'rb') as fp:
                seed = fp.read()
                fp.close()
            assert len(seed) > 0
            assert isinstance(seed, bytes)
            self._seed = [seed]
            print('[+] Use seed {}, length {}'.format(seed_path, len(seed)))
            self._input_maxsize = 32 * 1024
            self.reset()
        elif os.path.isdir(seed_path):
            seed_names = os.listdir(seed_path)
            self._seed = []
            for each in seed_names:
                if each.endswith(self._suffix):
                    with open(os.path.join(seed_path, each), 'rb') as fp:
                        seed = fp.read()
                        fp.close()
                    assert len(seed) > 0
                    assert isinstance(seed, bytes)
                    self._seed.append(seed)
                    print('[+] Use seed {}, length {}'.format(seed_path + each, len(seed)))
            self._input_maxsize = 32 * 1024
            self.reset()

    def set_peach_seed(self, seed_path):
        self._Seed_Path = seed_path
