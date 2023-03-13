
from ZZRFuzz_Cmplog import *
ByteDic = {}
def computeRate(init_cmp_map,cur_cmp_map,init_byte,cur_byte,cur_index):
    for i in range(65535):
        if cur_cmp_map.headers[i].type == CMP_TYPE_INS and init_cmp_map.headers[i].type == CMP_TYPE_INS:
            if cur_cmp_map.headers[i].hits == init_cmp_map.headers[i].hits:
                for j in range(min(cur_cmp_map.headers[i].hits,32)):
                    if init_cmp_map.log[i][j].v0 == init_byte and cur_cmp_map.log[i][j].v0 == cur_byte:
                        if cur_index not in ByteDic.keys():
                            ByteDic[cur_index] = [init_cmp_map.log[i][j].v1]
                            ByteDic[cur_index].append(cur_cmp_map.log[i][j].v1)
                            #ByteDic[i] = list(set(lst1))
                        else:
                            ByteDic[cur_index].append(cur_cmp_map.log[i][j].v1)
                            ByteDic[cur_index].append(init_cmp_map.log[i][j].v1)
                    elif init_cmp_map.log[i][j].v1 == init_byte and cur_cmp_map.log[i][j].v1 == cur_byte:
                        if cur_index not in ByteDic.keys():
                            ByteDic[cur_index] = [init_cmp_map.log[i][j].v0]
                            ByteDic[cur_index].append(cur_cmp_map.log[i][j].v0)
                            #ByteDic[i] = list(set(lst1))
                        else:
                            ByteDic[cur_index].append(cur_cmp_map.log[i][j].v0)
                            ByteDic[cur_index].append(init_cmp_map.log[i][j].v0)
    if cur_index in ByteDic.keys():
        ByteDic[cur_index] = list(set(ByteDic[cur_index]))


