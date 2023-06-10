import copy
import time
from ZZRFuzz.config import *
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

    seed_block.append([cur_start,len(cov_per_byte)])

    mutate_block_index = []
    for i in range(len(seed_block)):
        mutate_block_index.append(i)
    return seed_block,mutate_block_index
def mute_seed(in_seed_bytes, index):
    origin = in_seed_bytes[index]
    if in_seed_bytes[index] == 0xff:
        in_seed_bytes[index] = 0xfe
    else:
        in_seed_bytes[index] = origin + 1





def seedCrack(engine,seed_path):
    cov_per_byte = []
    crash_per_byte = []
    with open("/tmp/cmp_log_config", "w") as cmp_log_config:
        cmp_log_config.write("0")
    init_crack_mode = 1
    #fix 1 bug
    #seed_path = "cov__1__390"

    with open(seed_path, "rb") as in_seed_fp:
        in_seed_bytes = in_seed_fp.read()
        # test one
        init_cov,init_cmp_map = engine.run(in_seed_bytes)
        print(init_cov.transition_count())

        for i in range(len(in_seed_bytes)):

            print("cur i:"+str(i))

            if i %100 == 0:
                print("cur_index: "+str(i))
            mute_seed_bytes = copy.deepcopy(in_seed_bytes)
            mute_seed_bytes = bytearray(mute_seed_bytes)
            mute_seed(mute_seed_bytes, index=i)

            start_time = time.perf_counter()

            cur_cov,cur_cmp_map = engine.run(mute_seed_bytes)

            if cur_cov.transition_count() == 1:
                with open("cov__1__"+str(i),"wb") as fp:
                    print("found 1 cov")
                    fp.write(mute_seed_bytes)

            end_time = time.perf_counter()

            elapsed_time = (end_time - start_time) * 1000
            print(f"AFL run cost : {elapsed_time:.3f} ms")


            cov_per_byte.append(cur_cov.transition_count())
            crash_per_byte.append(cur_cov.crashes)

        print(cov_per_byte)
        print(crash_per_byte)

        (seed_block,mutate_block_index) = crack_seed(cov_per_byte)
        print(seed_block)

        seed_block = [[start_loc, end_loc - start_loc] for start_loc, end_loc in seed_block]
        print(seed_block)

        print(mutate_block_index)
    init_crack_mode = 1
    return (seed_block,mutate_block_index)