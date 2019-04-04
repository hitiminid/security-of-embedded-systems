from a51 import A5_1
import utils

class Cipher:

    def __init__(self, IV):
        self.a51 = A5_1(IV)
        self.frame_no = 0

    def perform_encryption(self, message_chunks):
        f_no = self.frame_no
        msg_length = len(message_chunks)
        self.frame_no += msg_length // 8
        bits = a51.get_bits(msg_length * 8)
        noises = list(utils.chunks(bits, 8))

        for chunk, noise in zip(message_chunks, noises):
            ciphertext = self.perform_xor(chunk, noise)

        return f_no, ciphertext

    def perform_xor(self, text, key):
        return [m ^ k for m, k in zip(text, key)]


    def perform_decryption(self, messages, frame_nos):
        decrypted_messages = []

        for ciphertext, frame_no in zip(messages, frame_nos):
            if not self.frame_no == frame_no:
                raise Exception('Wrong frame numbers!!!')
            self.frame_no += 1

            bits = a51.get_bits(8)
            decrypted_messages.append(perform_xor(ciphertext, bits))
        return decrypted_messages



# message = [1,0,1,0,1]
# key = [1,1,1,1,1]
# cipher = perform_encryption(message, key)
