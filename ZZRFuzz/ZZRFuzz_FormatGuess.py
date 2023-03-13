import ctypes

from ZZRFuzz_computeRate import *
from ZZRFuzz_forkclient import ForkClient
from ZZRFuzz_coverage import *
from ZZRFuzz_Cmplog import *
import copy
from config import *

in_seed_file = "in_afl/metadata.png"
out_iter_file = "out/iter.png"
init_cov = 0


cov_per_byte = []
crash_per_byte = []


def crack_seed(cov_per_byte):
    seed_block = []
    cur_start = 0
    cur_cov = cov_per_byte[0]
    for i in range(len(cov_per_byte)):
        if cov_per_byte[i] != cur_cov:
            seed_block.append([cur_start,i])
            cur_start = i
            cur_cov = cov_per_byte[i]

    seed_block.append([cur_start,len(cov_per_byte)+1])
    mutate_block_index = []
    for i in range(len(seed_block)):
        mutate_block_index.append(i)
    return seed_block
def mute_seed(in_seed_bytes, index):
    origin = in_seed_bytes[index]
    if in_seed_bytes[index] == 0xff:
        in_seed_bytes[index] = 0xfe
    else:
        in_seed_bytes[index] = origin + 1


if __name__ == "__main__":
    print(ctypes.sizeof(cmp_header))
    with open("/tmp/cmp_log_config", "w") as cmp_log_config:
        cmp_log_config.write("0")
    #exit(0)
    #AFL_client = Afl("/home/zzr/AFLplusplus/test_cmp_log",["@@"])
    AFL_client = Afl("/home/zzr/AFLplusplus/pngquant_ori", ["-f","@@","-o","out.png"])
    with open(in_seed_file, "rb") as in_seed_fp:
        in_seed_bytes = in_seed_fp.read()
        # test one
        init_cov,init_cmp_map = AFL_client.run(in_seed_bytes)
        print(init_cov.transition_count())
        # with open("python_cmp.log","w") as fp:
        #     for i in range(65535):
        #         if cur_cmp_map.headers[i].type == CMP_TYPE_INS:
        #             for j in range(min(cur_cmp_map.headers[i].hits,32)):
        #                 fp.write("{0}.{1} : op1 -> {2} , op2 -> {3}\n".format(i,j,cur_cmp_map.log[i][j].v0,cur_cmp_map.log[i][j].v1))

        #init_cov = cur_cov.transition_count()

        for i in range(len(in_seed_bytes)):
            if i %100 == 0:
                print("cur_index: "+str(i))
            mute_seed_bytes = copy.deepcopy(in_seed_bytes)
            mute_seed_bytes = bytearray(mute_seed_bytes)
            mute_seed(mute_seed_bytes, index=i)

            start_time = time.perf_counter()

            cur_cov,cur_cmp_map = AFL_client.run(mute_seed_bytes)

            end_time = time.perf_counter()

            elapsed_time = (end_time - start_time) * 1000
            print(f"AFL run cost : {elapsed_time:.3f} ms")
            if cmp_log_flag:
                computeRate(init_cmp_map,cur_cmp_map,in_seed_bytes[i],mute_seed_bytes[i],i)

            cov_per_byte.append(cur_cov.transition_count())
            crash_per_byte.append(cur_cov.crashes)

        print(cov_per_byte)
        print(crash_per_byte)
        print(ByteDic)

        seed_block = crack_seed(cov_per_byte)
        print(seed_block)
    exit(0)


