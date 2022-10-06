import socket
import time

STATUS_OK = 0
STATUS_CRASHED = 0x80000000
STATUS_HANGED = 0x40000000
STATUS_ERROR = 0x20000000


class SocketEngine:
    def __init__(self, target_ip, target_port, comm_method):
        self.target_ip = target_ip
        self.target_port = target_port
        self.comm_method = comm_method

        if self.comm_method == 'TCP':
            self.control_port = 2187
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.control_socket.connect((self.target_ip, self.control_port))
        elif self.comm_method == 'UDP':
            self.control_port = 8005
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.control_socket.settimeout(3)
            self.control_socket.bind(('', self.control_port))

    def TCP_communicate(self, input_data, size):
        trans_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.send('s'.encode('utf-8'))
        trans_socket.connect((self.target_ip, self.target_port))
        trans_socket.send(input_data)
        time.sleep(0.5)
        self.control_socket.send('e'.encode('utf-8'))
        trans_socket.close()
        received_data1 = self.control_socket.recv(size)
        received_data2 = self.control_socket.recv(65536)
        status, data = self.recv_process(received_data1)
        # data = received_data2
        return (status, data)

    def UDP_communicate(self, input_data, size):

        trans_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        trans_socket.connect((self.target_ip, self.target_port))
        trans_socket.send(input_data)
        time.sleep(0.5)
        trans_socket.close()

        try:
            received_data, address = self.control_socket.recvfrom(size)
            status, data = self.recv_process(received_data)
            return (status, data)

        except socket.error as e:
            if e.errno == 10060:
                status = STATUS_CRASHED
                return (status, data)

    def recv_process(self, recv):
        if recv[0] == 0x38:
            status = STATUS_CRASHED
            data = recv
        else:
            status = STATUS_OK
            data = recv
        return status, data
