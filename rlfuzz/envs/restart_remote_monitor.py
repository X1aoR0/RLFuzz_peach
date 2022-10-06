import socket

import paramiko
import telnetlib
import argparse
import time


def restart_ssh(ip, port, user_name, PASS, startcommand):
    startcommand = 'nohup {}  > out.txt & tail -f out.txt'.format(startcommand)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 跳过了远程连接中选择‘是’的环节,
    ssh.connect(ip, port, user_name, PASS)

    stdin, stdout, stderr = ssh.exec_command('cd /www/')
    time.sleep(1)
    stdin, stdout, stderr = ssh.exec_command('kill -2 $(pidof monitor_ac68u)')
    time.sleep(1)
    stdin, stdout, stderr = ssh.exec_command('kill -9 $(pidof new_file_)')
    time.sleep(1)
    stdin, stdout, stderr = ssh.exec_command('../tmp/home/root/mem_close_arm')
    time.sleep(1)
    stdin, stdout, stderr = ssh.exec_command(startcommand, get_pty=True)

    while not stdout.channel.exit_status_ready():
        stdout.channel.settimeout(5)
        try:
            result = stdout.readline()
            print(result, end='')
        except socket.error:
            break
        if 'Address already in use' in result:
            stdin, stdout, stderr = ssh.exec_command('kill -2 $(pidof monitor_ac68u)')
            stdin, stdout, stderr = ssh.exec_command('kill -9 $(pidof new_file_)')
            stdin, stdout, stderr = ssh.exec_command(startcommand)

        if stdout.channel.exit_status_ready():
            result = stdout.readlines()
            print(result)
            if result != [] and '[File exists]' in result[-1]:
                stdin, stdout, stderr = ssh.exec_command('./mem_close_arm')
                stdin, stdout, stderr = ssh.exec_command(startcommand)
    ssh.close()
    return


def restart_telnet(ip, port, user_name, PASS, startcommand):
    ## todo
    finish = '# '
    tn = telnetlib.Telnet(ip)
    tn.read_until('login: ')
    tn.write(user_name + '\n')
    tn.read_until('Password: ')
    tn.write(PASS + '\n')

    tn.read_until(finish)
    tn.write('cd /tmp/upload\n')

    tn.read_until(finish)
    # ps | grep httpd | grep -v grep |grep -v dhttpd | awk '{print $1}'
    # ./main 1038 192.168.0.188 4314276
    tn.write(startcommand + '\n')
    tn.close()
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="remote connection with and your username and password through ssh or telnet")
    parser.add_argument('--method', '-m', help='ssh or telnet ,defult ssh', default='ssh')
    parser.add_argument('--usrname', '-u', help='username')
    parser.add_argument('--passwd', '-P', help='password')
    parser.add_argument('--ip', '-I', help='remote ip address')
    parser.add_argument('--port', '-p', help='remote port')
    parser.add_argument('--startcommand', '-s', help='complete command line of your monitor in ""')
    args = parser.parse_args()

    IP = args.ip
    PORT = args.port
    user_name = args.usrname
    PASS = args.passwd
    method = args.method
    command = args.startcommand

    assert method in ['telnet', 'ssh'], "[X]this method not support"

    if method == 'ssh':
        restart_ssh(IP, PORT, user_name, PASS, command)
    elif method == 'telnet':
        restart_telnet(IP, PORT, user_name, PASS, command)
