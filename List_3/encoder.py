import random
import subprocess

import utils


class Encoder:

    frame_number = 0
    FRAME_DATA_SIZE = 8
    FRAME_DATA_START = 2


    def __init__(self, iv):
        self.iv = iv


    @staticmethod
    def generate_IV():
        return random.getrandbits(64)


    def perform_encryption(self, message):
        bits = __get_vhdl_bits()
        encrypted_message = encrypt_message(message, bits)


    def __get_vhdl_bits(self):
        return bits


    def encrypt_message(self, message, bits):
        encrypted_message = utils.xor(message, bits)
        return encrypted_message


    def frame_data(self, message):
        chunks = list(utils.chunks(message, 8))
        is_last_chunk = [False] * (len(chunks)-1) + [True]

        frames = [self.__create_frame(chunk, is_last) for chunk, is_last
                  in zip(chunks, is_last_chunk)]
        return frames


    def __create_frame(self, message, is_last):
        frame = [255] # start
        frame += self.__create_frame_number()
        frame += self.__create_message(message)
        frame += self.__create_checksum(frame)
        frame += self.__create_ending(is_last)
        return frame


    def __create_frame_number(self):
        self.frame_number += 1
        frame_number_list = [
            self.frame_number
            # self.frame_number >> 24,
            # (self.frame_number << 8) >> 24,
            # (self.frame_number << 16) >> 24,
            # (self.frame_number << 24) >> 24
        ]
        return frame_number_list


    def __create_message(self, message):
        while len(message) < 8:
            message.append(0)
        return message


    def __create_checksum(self, frame):
        s, carry = self.__compute_checksum(frame)
        return [s, carry]


    def __compute_checksum(self, frame):
        s = 0
        carry = 0
        limit = self.FRAME_DATA_SIZE + self.FRAME_DATA_START

        for i in range(1, limit):
            if s + frame[i] > 255:
                carry += 1
            s = (s + frame[i]) % 256
        return s, carry


    def __check_checksum(self, frame):
        s, carry = __create_checksum(frame)
        return s == frame[10] and carry == frame[11] and frame[0] == 255 and (frame[12] == 0 or frame[12] == 255)


    def __create_ending(self, is_last):
        return [0] if is_last else [255]


# encoder = Encoder('s')
# message = [128, 128, 128, 128, 128, 128, 128, 128, 128]
# message = [255, 0, 128, 128, 128, 128, 128, 128, 128, 128, 13, 4, 0]
# frame = encoder.frame_data(message)
# import pdb; pdb.set_trace()
# print(check_sum)
