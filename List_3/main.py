# from communication import Communication
# from encoder import Encoder
# from a51 import A5_1


import serial
from time import sleep
import random
import cipher
import encoder

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

class Comm:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600)
        sleep(3)

    def calculate_checksum(self, frame):
        s = 0
        carry = 0
        for i in range(1,FRAME_DATA_SIZE+FRAME_DATA_START):
            s += frame[i]
            if (s >= 256):
                carry += 1
            s %= 256
        s = sum(frame[1:FRAME_DATA_SIZE+FRAME_DATA_START])
        carry = s//256
        s %= 256
        return (s,carry)

    def validate_frame(self, frame):
        (s,carry) = self.calculate_checksum(frame)
        return (s == frame[FRAME_CHECKSUM_START]
                and carry == frame[FRAME_CHECKSUM_START+1]
                and frame[0] == FRAME_START_BYTE
                and (frame[FRAME_SIZE-1] == FRAME_END_BYTE or frame[FRAME_SIZE-1] == FRAME_START_BYTE))

    def send_frame(self, frame):
        # print(frame)
        while True:
            for f in frame:
                self.ser.write(f.to_bytes(1, byteorder='big'))
                sleep(0.001)
            # print("Waiting for ACC")
            x = self.ser.read()
            # print(x)
            if x == b'k':
                break
            sleep(0.01)
        # print("Sended")

    def send_frames(self, frames):
        self.ser.write(SENDING_DATA.to_bytes(1, byteorder='big'))
        # print("Sended SENDING_DATA.to_bytes(1, byteorder='big')")
        x = self.ser.read()
        # print(x)
        if x == READY_SENDING_DATA.to_bytes(1, byteorder='big'):
            for frame in frames:
                self.send_frame(frame)
            return True
        else:
            return False

    def read_frame(self):
        while True:
            # frame = self.ser.read(13)
            # print(frame)
            # frame = [int.from_bytes(f, byteorder='big) for f in frame]
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
        self.ser.write(ASK_DATA_PENDING.to_bytes(1, byteorder='big'))
        x = self.ser.read()
        # print(x)
        if x != YES_DATA_PENDING.to_bytes(1, byteorder='big'):
            return []
        self.ser.write(REQUEST_PENDING_DATA.to_bytes(1, byteorder='big'))

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
# gen_and_send_iv

    def get_msg_from_frames(self, frames):
        msg = []
        for frame in frames:
            msg += frame[2:10]
        return msg

    def get_frame_nos_from_frames(self, frames):
        # nos = []
        # for frame in frames:
        #     nos.append(frame[1])
        return [frame[1] for frame in frames]

def perform_IV_exchange(c):
    print("[0] Gen and send IV")
    print("[1] Read IV")
    print("> ", end='')

    choice = input()

    if choice == "0":
        iv = c.gen_and_send_iv()
    elif choice == "1":
        iv = c.read_iv()

    print(iv)
    return iv


def communicate(c):
    print("[0] Send message")
    print("[1] Read message")
    print("> ", end='')

    choice = input()
    if choice == "0":
        msg = input()
        msg = [ord(m) for m in msg]
        split_padded_message = split_and_pad_data(msg)
        frames = Encoder.frame_data(split_padded_message)
        sleep(0.001)
        print(c.send_frames(frames))

    elif choice == "1":
        frames = c.read_frames()
        if (frames != []):
            msg = c.get_msg_from_frames(frames)
            frame_nos = c.get_frame_nos_from_frames(frames)
            msg = decrypt_message(msg, frame_nos)

            while (msg[-1] == '\x00'):
                msg = msg[:-1]
            print(''.join(msg))


def split_and_pad_data(message):
    chunks = list(utils.chunks(message, 8))
    while len(chunks[-1]) < 8:
        chunks[-1].append(0)
    return chunks


def decrypt_message(msg: list, frame_nos):
    msg = [chr(m) for m in msg]
    msg = cipher.perform_decryption(msg, frame_nos)
    return msg


def main():
    c = Comm("/dev/ttyUSB0")
    iv = perform_IV_exchange(c)
    Cipher = cipher.Cipher(iv)
    Encoder = encoder.Encoder(Cipher)

    while True:
        communicate(c)

if __name__ == "__main__":
    main()
