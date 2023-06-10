import os

from gym.envs.registration import register


def afl_forkserver_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/afl-2.52b-mod/afl-2.52b/afl-forkserver',
    )


def afl_2_57_forkserver_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/afl-2.57b-mod/afl-2.57b/afl-forkserver',
    )


# base64_afl
def base64_target_path():
    # package_directory = os.path.dirname(os.path.abspath(__file__))
    # return os.path.join(
    #     package_directory, 'mods/lava-m-mod/base64_afl',
    # )
    return "/home/zzr/RLFuzz_peach/rlfuzz/mods/lava-m-mod/base64_afl"


register(
    id='FuzzBase64-v0',
    entry_point='rlfuzz.envs:FuzzBase64Env',
)


# md5sum_afl
def md5sum_target_path():
    # package_directory = os.path.dirname(os.path.abspath(__file__))
    # return os.path.join(
    #     package_directory, 'mods/lava-m-mod/md5sum_afl',
    # )
    return "/home/zzr/RLFuzz_peach/rlfuzz/mods/lava-m-mod/md5sum_afl"


register(
    id='FuzzMd5sum-v0',
    entry_point='rlfuzz.envs:FuzzMd5sumEnv',
)


# uniq_afl
def uniq_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/lava-m-mod/uniq_afl',
    )


register(
    id='FuzzUniq-v0',
    entry_point='rlfuzz.envs:FuzzUniqEnv',
)


# who_afl
def who_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/lava-m-mod/who_afl',
    )


register(
    id='FuzzWho-v0',
    entry_point='rlfuzz.envs:FuzzWhoEnv',
)


# tar_afl

def gzip_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/gzip-mod/gzip_afl',
    )


register(
    id='Fuzzgzip-v0',
    entry_point='rlfuzz.envs:FuzzgzipEnv',
)


# libpng

def libpng_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return "/home/zzr/fuzzer-test-suite/libpng-1.2.56/build/libpng-coverage"


register(
    id='Fuzzlibpng-v0',
    entry_point='rlfuzz.envs:FuzzlibpngEnv',
)


# gueztil

def gueztil_target_path():
    # package_directory = os.path.dirname(os.path.abspath(__file__))
    # return os.path.join(
    #     package_directory, 'mods/fuzzer-test-suite-mod/programs/guetzli-2017-3-30-afl',
    #
    return "/home/zzr/fuzzer-test-suite-master/guetzli-2017-3-30/build/gue-afl"


register(
    id='Fuzzguetzil-v0',
    entry_point='rlfuzz.envs:FuzzguetzilEnv',
)


# libjpeg

def libjpeg_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    # return os.path.join(
    #     package_directory, 'mods/fuzzer-test-suite-mod/programs/libjpeg-turbo-07-2017-afl',
    # )
    return "/home/zzr/fuzzer-test-suite/libjpeg-turbo-07-2017/build/jpeg-coverage"
    #return "/home/zzr/RLFuzz_peach/teststderr"


register(
    id='Fuzzlibjpeg-v0',
    entry_point='rlfuzz.envs:FuzzlibjpegEnv',
)


# pngquant
def pngquant_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join("/home/zzr/AFLplusplus/pngquant_ori")


register(
    id='FuzzPngquant-v0',
    entry_point='rlfuzz.envs:FuzzpngquantEnv',
)


def cmptest_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join("/home/zzr/ZZR_AFL/AFLplusplus/test_cmp_log")


register(
    id='Fuzzcmptest-v0',
    entry_point='rlfuzz.envs:FuzzcmptestEnv',
)


# CImg
def CImg_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(
        package_directory, 'mods/Cimg-mod/image2ascii',
    )


register(
    id='FuzzCImg-v0',
    entry_point='rlfuzz.envs:FuzzCImgEnv',
)

def libxml2_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return "/home/zzr/fuzzer-test-suite/libxml2-v2.9.2/BUILD/libxml2-noinstru"


register(
    id='Fuzzlibxml2-v0',
    entry_point='rlfuzz.envs:Fuzzlibxml2Env',
)

def guetil_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return "/home/zzr/fuzzer-test-suite/guetzli-2017-3-30/guetil-noinstru"


register(
    id='Fuzzguetil-v0',
    entry_point='rlfuzz.envs:FuzzguetilEnv',
)

def libarchieve_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return "/home/zzr/fuzzer-test-suite/libarchive-2017-01-04/libarchieve-noinstru"


register(
    id='Fuzzlibarchieve-v0',
    entry_point='rlfuzz.envs:FuzzlibarchieveEnv',
)

def freetype2_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return "/home/zzr/fuzzer-test-suite/freetype2-2017/BUILD/freetype-instru"


register(
    id='Fuzzfreetype2-v0',
    entry_point='rlfuzz.envs:Fuzzfreetype2Env',
)

def harfbuzz_target_path():
    package_directory = os.path.dirname(os.path.abspath(__file__))
    return "/home/zzr/fuzzer-test-suite/harfbuzz-1.3.2/BUILD/harbuzz-noinstru"


register(
    id='Fuzzharfbuzz-v0',
    entry_point='rlfuzz.envs:FuzzharfbuzzEnv',
)



# user defined binary
register(
    id='UserDefined-v0',
    entry_point='rlfuzz.envs:FuzzUserDefinedEnv',
)

register(
    id='FUzzSocket-v0',
    entry_point='rlfuzz.envs:FuzzSocketEnv'
)

register(
    id='FuzzAC68U-v0',
    entry_point='rlfuzz.envs:FuzzAC68UEnv'
)

register(
    id='FuzzAC9-v0',
    entry_point='rlfuzz.envs:FuzzAC9Env'
)
