import random
import subprocess

import cipher
import utils


class Encoder:

    FRAME_DATA_SIZE = 8
    FRAME_DATA_START = 2

    def __init__(self, cipher):
        self.Cipher = cipher

    @staticmethod
    def generate_IV():
        return random.getrandbits(64)


    def frame_data(self, chunks):
        f_no, cipher_text = self.Cipher.perform_encryption(chunks)
        is_last_chunk = [False] * (len(chunks)-1) + [True]
        frames = []
        for chunk, is_last in zip(chunks, is_last_chunk):
            frames.append(self.__create_frame(chunk, is_last, f_no))
            f_no += 1
        return frames


    def __create_frame(self, message, is_last, f_no):
        frame = [255] # start
        frame += self.__create_frame_number(f_no)
        frame += self.__create_message(message)
        frame += self.__create_checksum(frame)
        frame += self.__create_ending(is_last)
        return frame


    def __create_frame_number(self, f_no):
        frame_number_list = [f_no]
        return frame_number_list


    def __create_message(self, message):
        # while len(message) < 8:
        #     message.append(0)
        # message, _ = cipher.perform_encryption(message, iv) # TODO: number ramki, ogarnąć!
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


    def __create_ending(self, is_last):
        return [0] if is_last else [255]
