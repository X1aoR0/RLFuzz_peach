import rlfuzz
from rlfuzz.envs.fuzz_base_env import FuzzBaseEnv

import os


class FuzzBase64Env(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.base64_target_path()
        self._args = ['-d']
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = ''
        self._set_out = []
        self._input_maxsize = 64 * 1024  # 最大输入文件的大小
        self.seed_names = []
        self._dataModelName = 'blank'
        self._PitPath = 'file:test/pit/Blank.xml'
        super(FuzzBase64Env, self).__init__()

    def set_seed(self, seed_path):
        if os.path.isfile(seed_path):
            with open(seed_path, 'rb') as fp:
                seed = fp.read()
                fp.close()
            assert len(seed) > 0
            assert isinstance(seed, bytes)
            self._seed = [seed]
            print('[+] Use seed {}, length {}'.format(seed_path, len(seed)))
            self._input_maxsize = 64 * 1024
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
            self._input_maxsize = 64 * 1024
            self.reset()

    def set_peach_seed(self, seed_path):
        self._Seed_Path = seed_path


class FuzzMd5sumEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.md5sum_target_path()
        self._args = ['-c']
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = ''
        self._set_out = []
        self._dataModelName = 'blank'
        self._PitPath = 'file:test/pit/Blank.xml'
        self._input_maxsize = 64 * 1024  # 最大输入文件的大小
        self.seed_names = []
        super(FuzzMd5sumEnv, self).__init__()

    def set_seed(self, seed_path):
        if os.path.isfile(seed_path):
            with open(seed_path, 'rb') as fp:
                seed = fp.read()
                fp.close()
            assert len(seed) > 0
            assert isinstance(seed, bytes)
            self._seed = [seed]
            print('[+] Use seed {}, length {}'.format(seed_path, len(seed)))
            self._input_maxsize = 64 * 1024
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
            self._input_maxsize = 64 * 1024
            self.reset()

    def set_peach_seed(self, seed_path):
        self._Seed_Path = seed_path


class FuzzUniqEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.uniq_target_path()
        self._args = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = ''
        self._input_maxsize = 64 * 1024  # 最大输入文件的大小
        self.seed_names = []
        super(FuzzUniqEnv, self).__init__()

    def set_seed(self, seed_path):
        if os.path.isfile(seed_path):
            with open(seed_path, 'rb') as fp:
                seed = fp.read()
                fp.close()
            assert len(seed) > 0
            assert isinstance(seed, bytes)
            self._seed = [seed]
            print('[+] Use seed {}, length {}'.format(seed_path, len(seed)))
            self._input_maxsize = 64 * 1024
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
            self._input_maxsize = 64 * 1024
            self.reset()

    def set_peach_seed(self, seed_path):
        self._Seed_Path = seed_path


class FuzzWhoEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.who_target_path()
        self._args = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = ''
        self._input_maxsize = 64 * 1024  # 最大输入文件的大小
        self.seed_names = []
        super(FuzzWhoEnv, self).__init__()

    def set_seed(self, seed_path):
        if os.path.isfile(seed_path):
            with open(seed_path, 'rb') as fp:
                seed = fp.read()
                fp.close()
            assert len(seed) > 0
            assert isinstance(seed, bytes)
            self._seed = [seed]
            print('[+] Use seed {}, length {}'.format(seed_path, len(seed)))
            self._input_maxsize = 64 * 1024
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
            self._input_maxsize = 64 * 1024
            self.reset()

    def set_peach_seed(self, seed_path):
        self._Seed_Path = seed_path


class FuzzgzipEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.gzip_target_path()
        self._args = ['-d']
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = '.gz'
        self._set_out = []
        self._input_maxsize = 64 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._dataModelName = 'gzip_file'
        self._PitPath = 'file:test/pit/GZIP_DataModel.xml'
        self.seed_names = []
        super(FuzzgzipEnv, self).__init__()

    def set_seed(self, seed_path):
        if os.path.isfile(seed_path):
            with open(seed_path, 'rb') as fp:
                seed = fp.read()
                fp.close()
            assert len(seed) > 0
            assert isinstance(seed, bytes)
            self._seed = [seed]
            print('[+] Use seed {}, length {}'.format(seed_path, len(seed)))
            self._input_maxsize = 64 * 1024
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
            self._input_maxsize = 64 * 1024
            self.reset()

    def set_peach_seed(self, seed_path):
        self._Seed_Path = seed_path


class FuzzpngquantEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.pngquant_target_path()
        self._args = ['-f']
        self._set_out = ['-o', '/tmp/out.png']
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = '.png'
        self._input_maxsize = 64 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._dataModelName = 'PNG'
        self._PitPath = 'file:test/pit/png_datamodel.xml'
        self.seed_names = []
        super(FuzzpngquantEnv, self).__init__()

    def set_seed(self, seed_path):
        if os.path.isfile(seed_path):
            with open(seed_path, 'rb') as fp:
                seed = fp.read()
                fp.close()
            assert len(seed) > 0
            assert isinstance(seed, bytes)
            self._seed = [seed]
            print('[+] Use seed {}, length {}'.format(seed_path, len(seed)))
            self._input_maxsize = 64 * 1024
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
                    print('[+] Use seed {}, length {}'.format(seed_path + '/' + each, len(seed)))
            self._input_maxsize = 64 * 1024
            self.reset()

    def set_peach_seed(self, seed_path):
        self._Seed_Path = seed_path



class FuzzlibPngEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.pngquant_target_path()
        self._args = ['']
        self._set_out = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = '.png'
        self._input_maxsize = 64 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._dataModelName = 'PNG'
        self._PitPath = 'file:test/pit/png_datamodel.xml'
        self.seed_names = []
        super(FuzzlibPngEnv, self).__init__()

    def set_seed(self, seed_path):
        if os.path.isfile(seed_path):
            with open(seed_path, 'rb') as fp:
                seed = fp.read()
                fp.close()
            assert len(seed) > 0
            assert isinstance(seed, bytes)
            self._seed = [seed]
            print('[+] Use seed {}, length {}'.format(seed_path, len(seed)))
            self._input_maxsize = 64 * 1024
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
                    print('[+] Use seed {}, length {}'.format(seed_path + '/' + each, len(seed)))
            self._input_maxsize = 64 * 1024
            self.reset()

    def set_peach_seed(self, seed_path):
        self._Seed_Path = seed_path


class FuzzCImgEnv(FuzzBaseEnv):
    def __init__(self):
        self._target_path = rlfuzz.CImg_target_path()
        self._args = ['-i']
        self._set_out = []
        self._seed = [b'']  # 指定初始变异的文件
        self._suffix = '.bmp'
        self._input_maxsize = 64 * 1024  # 最大输入文件的大小
        self._Seed_Path = ''
        self._dataModelName = 'BMP'
        self._PitPath = 'file:test/pit/BMP_DataModel.xml'
        self.seed_names = []
        super(FuzzCImgEnv, self).__init__()

    def set_seed(self, seed_path):
        if os.path.isfile(seed_path):
            with open(seed_path, 'rb') as fp:
                seed = fp.read()
                fp.close()
            assert len(seed) > 0
            assert isinstance(seed, bytes)
            self._seed = [seed]
            print('[+] Use seed {}, length {}'.format(seed_path, len(seed)))
            self._input_maxsize = 64 * 1024
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
                    print('[+] Use seed {}, length {}'.format(seed_path + '/' + each, len(seed)))
            self._input_maxsize = 64 * 1024
            self.reset()

    def set_peach_seed(self, seed_path):
        self._Seed_Path = seed_path
