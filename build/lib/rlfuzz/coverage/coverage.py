import numpy as np

import operator
from rlfuzz.coverage.forkclient import ForkClient
from rlfuzz.coverage.forkclient import STATUS_CRASHED
from rlfuzz.coverage.socketengine import SocketEngine

PATH_MAP_SIZE = 2 ** 16
MAP_SIZE_SOCKET = 12016


class Coverage:
    def __init__(self, coverage_status=None, coverage_data=None, verbose=False, socket_flag=False):
        self.crashes = 0
        self.verbose = verbose
        self.socket_flag = socket_flag

        assert coverage_status is not None
        assert coverage_data is not None

        if coverage_status == STATUS_CRASHED:
            self.crashes = 1

        if socket_flag:
            self.coverage_data = np.array([each for each in coverage_data], dtype=np.uint8)
        else:
            self.coverage_data = np.array(
                list(map(self.classify_counts, coverage_data)), dtype=np.uint8)

    # Reward
    def reward(self):
        if self.socket_flag:
            return self.none_zero_bits_count() / (len(self.coverage_data) * 8)
        return self.transition_count() / PATH_MAP_SIZE

    # 运行时经过的跳转数（不重复计算）
    def transition_count(self):
        return np.nonzero(self.coverage_data)[0].shape[0]

    def none_zero_bits_count(self):
        res = 0
        for each in self.coverage_data:
            for i in range(8):
                res += each >> i & 0x01
        return res

    # classify_counts 对原始 coverage_data 进行预处理
    def classify_counts(self, a):
        assert 0 <= a <= 255
        if a == 0:
            return 0
        elif a == 1:
            return 1
        elif a == 2:
            return 2
        elif a == 3:
            return 4
        elif 4 <= a <= 7:
            return 8
        elif 8 <= a <= 15:
            return 16
        elif 16 <= a <= 31:
            return 32
        elif 32 <= a <= 127:
            return 64
        else:
            return 128


"""
AFL ENGINE
"""


class Afl:
    def __init__(self, target_path, args=[], suffix=None, verbose=False):
        self.verbose = verbose
        self.fc = ForkClient(target_path, args, suffix)

    def run(self, input_data):
        (status, data) = self.fc.run(input_data)
        return Coverage(status, data, self.verbose)


"""
Socket TCP communication
"""


class SocketComm:
    def __init__(self, target_ip, target_port, comm_method, verbose=False):
        self.verbose = verbose
        self.target_ip = target_ip
        self.target_port = target_port
        self.comm_method = comm_method
        self.s = SocketEngine(target_ip, target_port, self.comm_method)

    def run(self, input_data):
        if self.comm_method == 'TCP':
            (status, data) = self.s.TCP_communicate(input_data, MAP_SIZE_SOCKET)
            return Coverage(status, data, self.verbose, socket_flag=True)
        elif self.comm_method == 'UDP':
            (status, data) = self.s.UDP_communicate(input_data, MAP_SIZE_SOCKET)
            return Coverage(status, data, self.verbose, socket_flag=True)
