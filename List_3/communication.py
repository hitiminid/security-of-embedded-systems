import serial
from time import sleep
import random

class Communication:

    MAX_FRAME_NO = 32
    FRAME_MAX = 416
    FRAME_SIZE = 13
    FRAME_DATA_START = 2
    FRAME_DATA_SIZE = 8
    FRAME_CHECKSUM_START = 10
    FRAME_START_BYTE = 255
    FRAME_END_BYTE = 0
    ASK_DATA_PENDING = 100
    NO_DATA_PENDING = 101
    YES_DATA_PENDING = 102
    REQUEST_PENDING_DATA = 103
    SENDING_DATA = 200
    READY_SENDING_DATA = 201
    NOT_READY_SENDING_DATA = 202

    def __init__(self, port):
        self.ser = serial.Serial(port, 9600)
        sleep(3)

    def calculate_checksum(self, frame):
        s = 0
        carry = 0
        for i in range(1, self.FRAME_DATA_SIZE + self.FRAME_DATA_START):
            s += frame[i]
            if (s >= 256):
                carry += 1
            s %= 256
        s = sum(frame[1:self.FRAME_DATA_SIZE + self.FRAME_DATA_START])
        carry = s//256
        s %= 256
        return (s,carry)

    def validate_frame(self, frame):
        (s,carry) = self.calculate_checksum(frame)
        return (s == frame[self.FRAME_CHECKSUM_START]
                and carry == frame[self.FRAME_CHECKSUM_START+1]
                and frame[0] == self.FRAME_START_BYTE
                and (frame[self.FRAME_SIZE-1] == self.FRAME_END_BYTE or frame[self.FRAME_SIZE-1] == self.FRAME_START_BYTE))

    def send_frame(self, frame):
        while True:
            for f in frame:
                self.ser.write(f.to_bytes(1, byteorder='big'))
                sleep(0.001)
            x = self.ser.read()
            if x == b'k':
                break
            sleep(0.01)

    def send_frames(self, frames):
        self.ser.write(self.SENDING_DATA.to_bytes(1, byteorder='big'))
        x = self.ser.read()
        if x == self.READY_SENDING_DATA.to_bytes(1, byteorder='big'):
            for frame in frames:
                self.send_frame(frame)
            return True
        else:
            return False

    def read_frame(self):
        while True:
            frame = []
            for i in range(0,13):
                frame.append(int.from_bytes(self.ser.read(), byteorder='big'))

            if self.validate_frame(frame):
                break
            self.ser.write(b'\x01')
        self.ser.write(b'k')
        return frame


    def read_frames(self):
        frames = []
        self.ser.write(self.ASK_DATA_PENDING.to_bytes(1, byteorder='big'))
        x = self.ser.read()
        if x != self.YES_DATA_PENDING.to_bytes(1, byteorder='big'):
            return []
        self.ser.write(self.REQUEST_PENDING_DATA.to_bytes(1, byteorder='big'))

        while True:
            frame = self.read_frame()
            frames.append(frame)
            if frame[12] == 0:
                break
        return frames

    def prepare_frames(self, msg):
        frames = []

        while msg != []:
            frame = [0 for i in range(0,13)]
            frame[0] = 255
            frame[1] = 1
            frame[12] = 255
            for i in range(2,10):
                frame[i] = msg[i-2]
            (s,c) = self.calculate_checksum(frame)
            frame[10] = s
            frame[11] = c
            msg = msg[8:]
            if len(msg):
                frame[12] = 255
            else:
                frame[12] = 0
            frames.append(frame)

        return frames

    def gen_and_send_iv(self):
        iv = [random.randint(0, 255) for i in range(0, 8)]

        frame = self.prepare_frames(iv)[0]
        frame[1] = 0
        frame[10] -= 1
        if frame[10] < 0:
            frame[11] -= 1
            frame[10] += 256

        self.send_frame(frame)
        return iv

    def read_iv(self):
        frame = self.read_frame()
        return self.get_msg_from_frames([frame])

    def get_msg_from_frames(self, frames):
        msg = []
        for frame in frames:
            msg += frame[2:10]
        return msg

    def get_frame_nos_from_frames(self, frames):
        return [frame[1] for frame in frames]
