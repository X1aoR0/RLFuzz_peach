import rlfuzz
from rlfuzz.envs.fuzz_base_env import FuzzBaseEnv
import os


class FuzzlibpngEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.libpng_target_path()
        self._args = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = '.png'
        self._set_out = []
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self.seed_names = []
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
            self.seed_names = os.listdir(seed_path)
            self._seed = []
            for each in self.seed_names:
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


class FuzzguetzilEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.gueztil_target_path()
        self._args = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = '.jpg'
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._set_out = []
        self.seed_names = []
        self._dataModelName = 'JPGData'
        self._PitPath = 'file:test/pit/JPG_DataModel.xml'
        self.seed_names = []
        super(FuzzguetzilEnv, self).__init__()

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
            seed_map = {}
            for name in seed_names:
                size = os.path.getsize(os.path.join(seed_path, name))
                if size > self._input_maxsize:
                    continue
                seed_map.setdefault(name, size)
            seed_names = sorted(seed_map.items(), key=lambda d: d[1])
            self.seed_names = [i[0] for i in seed_names]
            self._seed = []
            for each in self.seed_names:
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


class FuzzlibjpegEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.libjpeg_target_path()
        self._args = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = '.jpg'
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._set_out = []
        self.seed_names = []
        self._dataModelName = 'JPGData'
        self._PitPath = 'file:test/pit/JPG_DataModel.xml'
        self.seed_names = []
        super(FuzzlibjpegEnv, self).__init__()

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
            seed_map = {}
            for name in seed_names:
                size = os.path.getsize(os.path.join(seed_path, name))
                if size > self._input_maxsize:
                    continue
                seed_map.setdefault(name, size)
            seed_names = sorted(seed_map.items(), key=lambda d: d[1])
            self.seed_names = [i[0] for i in seed_names]
            self._seed = []
            for each in self.seed_names:
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



class Fuzzlibxml2Env(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.libxml2_target_path()
        self._args = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = '.xml'
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._set_out = []
        self.seed_names = []
        self._dataModelName = 'JPGData'
        self._PitPath = 'file:test/pit/JPG_DataModel.xml'
        self.seed_names = []
        super(Fuzzlibxml2Env, self).__init__()

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
            seed_map = {}
            for name in seed_names:
                size = os.path.getsize(os.path.join(seed_path, name))
                if size > self._input_maxsize:
                    continue
                seed_map.setdefault(name, size)
            seed_names = sorted(seed_map.items(), key=lambda d: d[1])
            self.seed_names = [i[0] for i in seed_names]
            self._seed = []
            for each in self.seed_names:
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


class FuzzguetilEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.guetil_target_path()
        self._args = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = ''
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._set_out = []
        self.seed_names = []
        self._dataModelName = 'JPGData'
        self._PitPath = 'file:test/pit/JPG_DataModel.xml'
        self.seed_names = []
        super(FuzzguetilEnv, self).__init__()

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
            seed_map = {}
            for name in seed_names:
                size = os.path.getsize(os.path.join(seed_path, name))
                if size > self._input_maxsize:
                    continue
                seed_map.setdefault(name, size)
            seed_names = sorted(seed_map.items(), key=lambda d: d[1])
            self.seed_names = [i[0] for i in seed_names]
            self._seed = []
            for each in self.seed_names:
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


class FuzzlibarchieveEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.libarchieve_target_path()
        self._args = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = ''
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._set_out = []
        self.seed_names = []
        self._dataModelName = 'JPGData'
        self._PitPath = 'file:test/pit/JPG_DataModel.xml'
        self.seed_names = []
        super(FuzzlibarchieveEnv, self).__init__()

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
            seed_map = {}
            for name in seed_names:
                size = os.path.getsize(os.path.join(seed_path, name))
                if size > self._input_maxsize:
                    continue
                seed_map.setdefault(name, size)
            seed_names = sorted(seed_map.items(), key=lambda d: d[1])
            self.seed_names = [i[0] for i in seed_names]
            self._seed = []
            for each in self.seed_names:
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




class Fuzzfreetype2Env(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.freetype2_target_path()
        self._args = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = ''
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._set_out = []
        self.seed_names = []
        self._dataModelName = 'JPGData'
        self._PitPath = 'file:test/pit/JPG_DataModel.xml'
        self.seed_names = []
        super(Fuzzfreetype2Env, self).__init__()

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
            seed_map = {}
            for name in seed_names:
                size = os.path.getsize(os.path.join(seed_path, name))
                if size > self._input_maxsize:
                    continue
                seed_map.setdefault(name, size)
            seed_names = sorted(seed_map.items(), key=lambda d: d[1])
            self.seed_names = [i[0] for i in seed_names]
            self._seed = []
            for each in self.seed_names:
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


class FuzzharbuzzEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.harfbuzz_target_path()
        self._args = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = ''
        self._input_maxsize = 32 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._set_out = []
        self.seed_names = []
        self._dataModelName = 'JPGData'
        self._PitPath = 'file:test/pit/JPG_DataModel.xml'
        self.seed_names = []
        super(FuzzharbuzzEnv, self).__init__()

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
            seed_map = {}
            for name in seed_names:
                size = os.path.getsize(os.path.join(seed_path, name))
                if size > self._input_maxsize:
                    continue
                seed_map.setdefault(name, size)
            seed_names = sorted(seed_map.items(), key=lambda d: d[1])
            self.seed_names = [i[0] for i in seed_names]
            self._seed = []
            for each in self.seed_names:
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