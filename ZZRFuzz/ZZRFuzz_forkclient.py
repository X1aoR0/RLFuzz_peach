import mmap
import struct
import random
import time
import tempfile
import os
import signal
import subprocess
import threading
import datetime
import base64

from posix_ipc import SharedMemory, Semaphore, ExistentialError
from config import cmp_log_flag
def afl_forkserver_path():
    return "/home/zzr/ZZR_AFL/AFLplusplus/afl-fuzz"

# 最大输入大小
MAX_INPUT_SIZE = (2**24)  # 16M
MAP_SIZE = (2**16)
CMP_MAP_SIZE = 1032*65536
_ping_struc_hdr = "<II"
_pong_struc = "<II"
CMP_MAP_USE_FLAG_MAP_SIZE = 30
CMP_MAP_FINISH_FLAG_MAP_SIZE = 30
_mm_use = None

# compute this only once
_ping_struc_hdr_size = struct.calcsize(_ping_struc_hdr)
_pong_struc_size = struct.calcsize(_pong_struc)

STATUS_OK = 0
STATUS_CRASHED = 0x80000000
STATUS_HANGED = 0x40000000
STATUS_ERROR = 0x20000000

_lock = threading.Lock()

_process = None
_target_path = None

_shm = None
_mm = None
_ping_sem = None
_pong_sem = None

_clients = {}
_next_client_id = 0




def start_target_forkserver(command,env):
    global _process
    _process = subprocess.Popen(command,env=env, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
    while True:
        output = _process.stdout.readline()
        #output = _process.stderr.readline()
        if output == b'' and _process.poll() is not None:
            break
        if output:
            print(output.strip())





class ForkClient:
    def __init__(self, target_path, args=[]):
        global _lock
        global _process
        global _target_path
        global _shm
        global _mm
        global _ping_sem
        global _pong_sem
        global _clients
        global _next_client_id

        self.SEM_PING_SIGNAL_NAME = "/afl-ping-signal"
        self.SEM_PONG_SIGNAL_NAME = "/afl-pong-signal"
        self.SHARED_MEM_NAME = "/afl-shared-mem"

        # 随机化NAME来支持多进程
        self.randStr = base64.b64encode(str(datetime.datetime.now()).encode()).decode()
        self.SHARED_MEM_NAME += self.randStr
        self.SEM_PING_SIGNAL_NAME += self.randStr
        self.SEM_PONG_SIGNAL_NAME += self.randStr

        launch_afl_forkserver = True if _shm is None else False

        with _lock:
            self.client_id = _next_client_id
            _next_client_id += 1

            if launch_afl_forkserver:
                if _process is None:
                    env = os.environ.copy()
                    env["AFL_NO_AFFINITY"] = "1"
                    env["AFL_DEBUG"] = "1"
                    print(env)
                    # 不指定外部AFL_FORKSERVER 就用默认的SERVER
                    if 'EXTERNAL_AFL_FORKSERVER' not in env:
                        print("Starting afl-forkserver...")

                        fd, afl_out_file = tempfile.mkstemp(suffix='afl_out_file')
                        os.close(fd)

                        FNULL = open(os.devnull, 'w')
                        #AFL的启动参数
                        cmd = [
                            afl_forkserver_path(),
                            '-i',"/home/zzr/ZZRFuzz/in_afl",
                            '-o',"/home/zzr/ZZRFuzz/out_afl",
                            '-O',
                            '-r', self.randStr,
                            '-c',
                            '0',
                            '--',
                            target_path,
                        ]
                        cmd += args
                        #cmd += ['@@']

                        # 输出cmd
                        print(' '.join(cmd))
                        t = threading.Thread(target=start_target_forkserver, args=(' '.join(cmd),env))
                        t.start()
                        # _process = subprocess.Popen(
                        #     cmd,
                        #     env=env,
                        #     #stdout=FNULL,
                        #     stdout=subprocess.STDOUT,
                        #     stderr=subprocess.STDOUT,
                        # )

                    _target_path = target_path

                    time.sleep(1)

                    while True:
                        try:
                            # 打开已经存在的共享内存
                            _shm = SharedMemory(self.SHARED_MEM_NAME)
                            break
                        except ExistentialError as e:
                            print('[!] ERROR: {} {}'.format(e, self.SHARED_MEM_NAME))
                            time.sleep(1)

                    print('_shm id = {}'.format(_shm.fd))

                    _mm = mmap.mmap(_shm.fd, 0)

                    _ping_sem = Semaphore(self.SEM_PING_SIGNAL_NAME)
                    _pong_sem = Semaphore(self.SEM_PONG_SIGNAL_NAME)
                else:
                    if target_path != _target_path:
                        raise Exception("Concurrent targets is not supported: {} {}"
                            .format(target_path, _target_path,),
                        )

            else:
                print("Skipping afl-forkserver start.")

            _clients[self.client_id] = True


    def __del__(self):
        global _clients

        with _lock:
            if self.client_id in _clients:
                del _clients[self.client_id]
            if len(_clients.keys()) == 0:
                if _process is not None:
                    _process.terminate()

    def make_ping(self, msgid, input):
        """
        .--------------------.
        |    PING message    |
        |--------------------|
        | uint32 msgid       |
        | uint32 size        |
        | uint8  input[size] |
        '--------------------'
        """
        assert (len(input) <= MAX_INPUT_SIZE)

        msg = struct.pack(
            _ping_struc_hdr + str(len(input)) + "s", msgid, len(input), input,
        )
        return msg

    def get_pong(self, msg):
        """
        .--------------------------.
        |      PONG message        |
        |--------------------------|
        | uint32 msgid (same)      |
        | uint32 status            |
        | uint8  trace_bits[MAP_SIZE]   |
        | uint8  cmp_log[MAP_SIZE]   |
        '--------------------------'
        """
        (msgid, status) = struct.unpack(_pong_struc, msg[:_pong_struc_size])
        data = msg[_pong_struc_size:_pong_struc_size+MAP_SIZE]
        if cmp_log_flag:
            cmp_log = msg[_pong_struc_size+MAP_SIZE:_pong_struc_size+MAP_SIZE+CMP_MAP_SIZE]
        else:
            cmp_log = None
        return (msgid, status, data,cmp_log)
        #return (msgid, status, data)

    def run(self, input_data):
        with _lock:
            msgid_ping = random.randint(0, 1000)
            ping_msg = self.make_ping(msgid_ping, input_data)

            _mm.seek(0)
            _mm.write(ping_msg)

            # tell server that a ping is ready
            _ping_sem.release()

            # Wait for server to proceed with input
            # do anything while waiting for server...

            # Is there a pong ready?
            _pong_sem.acquire()

            (msgid, status, data,cmp_log) = self.get_pong(_mm)

            return (status, data,cmp_log)


def signal_handler(signal, frame):
    global _process

    if _process is not None:
        _process.terminate()


signal.signal(signal.SIGINT, signal_handler)
