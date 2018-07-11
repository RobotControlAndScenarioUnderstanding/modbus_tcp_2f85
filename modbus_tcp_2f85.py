from pymodbus.client.sync import ModbusTcpClient
from math import ceil
from time import sleep
import threading


class Gripper:
    def __init__(self, address):
        self.client = ModbusTcpClient(address)
        self.lock = threading.Lock()

    def disconnect(self):
        self.client.close()

    def activate(self):
        self.send_cmd(self.gripper_cmd(1, 0, 0, 0, 0, 0))
        sleep(5)

    def open(self):
        self.send_cmd(self.gripper_cmd(1, 1, 0, 0xFF, 0xFF, 0xFF))

    def close(self):
        self.send_cmd(self.gripper_cmd(1, 1, 0, 0x00, 0xFF, 0xFF))

    @staticmethod
    def gripper_cmd(ract, rgto, ratr, rpr, rsp, rfr):
        cmd = [0, 0, 0, 0, 0, 0]
        cmd[0] = (ract & 0x1) | ((rgto << 0x3) & 0x8) | ((ratr << 0x4) & 0x10)
        cmd[3] = rpr
        cmd[4] = rsp
        cmd[5] = rfr
        # for i in cmd: print(hex(i))
        return cmd

    def send_cmd(self, data):
        if len(data) % 2 == 1:
            data.append(0)

        message = []

        for i in range(0, int(len(data) / 2)):
            message.append((data[2*i] << 8) + data[2 * i + 1])

        with self.lock:
            self.client.write_registers(0, message)

    def get_status(self, nbytes):
        nregs = int(ceil(nbytes / 2.0))
        with self.lock:
            response = self.client.read_input_registers(0, nregs)

        output = []

        for i in range(0, nregs):
            output.append((response.getRegister(i) & 0xFF00) >> 8)
            output.append(response.getRegister(i) & 0x00FF)

        return output
