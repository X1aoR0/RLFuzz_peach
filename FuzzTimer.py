import time
import os
import subprocess
import shutil



#python3 comparison.py -e Fuzzlibjpeg-v0 -m ddpg --use_seed --peach --pit /home/zzr/RLFuzz_peach/rlfuzz/test/pit/png_datamodel.xml

# # 将源文件拷贝到目标目录
# shutil.copy2(source_path, target_dir)
# 目标程序
target_program_path = "comparison.py"

# 创建文件夹
def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        pass

# 获取当前时间
def get_current_time():
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())

# 启动目标程序
def start_target_program():
    return subprocess.Popen(["python3", target_program_path,"-e","Fuzzlibpng-v0",
                             "-m","ddpg",
                             "--use_seed",
                             "--peach",
                             "--pit",
                             "/home/zzr/RLFuzz_peach/rlfuzz/test/pit/png_datamodel.xml"])

# 终止目标程序
def stop_target_program(process):
    if process.poll() is None:
        process.terminate()

# 主函数
if __name__ == "__main__":
    # 创建起始文件夹
    #create_folder("1")
    count = 0
    max_count = 5  # 运行最大次数
    target_process = None
    # 源文件路径
    source_path1 = "fuzz_cov.txt"
    source_path2 = "ddpg_Fuzzlibpng-v0_weights_actor.h5f.data-00000-of-00001"
    source_path3 = "ddpg_Fuzzlibpng-v0_weights_actor.h5f.index"
    source_path4 = "ddpg_Fuzzlibpng-v0_weights_critic.h5f.data-00000-of-00001"
    source_path5 = "ddpg_Fuzzlibpng-v0_weights_critic.h5f.index"

    while count < max_count:
        print("exec count{0}".format(count))
        # 启动目标程序
        target_process = start_target_program()

        # 创建新的文件夹
        count += 1
        folder_name = str(count)
        create_folder(folder_name)
        # 目标目录路径
        target_dir = folder_name
        # 休眠12小时
        time.sleep(12*60 * 60)
        # 终止目标程序
        if target_process is not None:
            stop_target_program(target_process)

        # file_path = os.path.join(folder_name, file_name)
        # with open(file_path, "w") as f:
        #     f.write("这是本次运行的输出结果。")
        if os.path.exists(source_path1):
            subprocess.run(["mv", source_path1, target_dir])
        if os.path.exists(source_path2):
            subprocess.run(["mv", source_path2, target_dir])
        if os.path.exists(source_path3):
            subprocess.run(["mv", source_path3, target_dir])
        if os.path.exists(source_path4):
            subprocess.run(["mv", source_path4, target_dir])
        if os.path.exists(source_path5):
            subprocess.run(["mv", source_path5, target_dir])
    print("five execs Finish..............")