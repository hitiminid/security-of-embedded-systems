from a51 import A5_1
import utils
import pdb

class Cipher:

    def __init__(self, IV):
        self.a51 = A5_1(IV)
        self.frame_no = 0

    def perform_encryption(self, message_chunks):
        f_no = self.frame_no
        msg_length = len(message_chunks)
        self.frame_no += msg_length
        encoded = []

        for message_chunk in message_chunks:
            bits = self.a51.get_bits(len(message_chunk) * 8)
            chunked_bits = list(utils.chunks(bits, 8))
            chunked_bits = [self.chunk_to_int(chunk) for chunk in chunked_bits]
            ciphertext = self.perform_xor(message_chunk, chunked_bits)
            encoded.append(ciphertext)

        return f_no, encoded

    def chunk_to_int(self,chunk):
        chunk = [str(i) for i in chunk]
        chunk = ''.join(chunk)
        return int(chunk,2)

    def perform_xor(self, text, key):
        return [m ^ k for m, k in zip(text, key)]

    def perform_decryption(self, messages, frame_nos):
        decrypted_messages = []

        for ciphertext, frame_no in zip(messages, frame_nos):
            if not self.frame_no == frame_no:
                raise Exception('Wrong frame numbers!!!')
            self.frame_no += 1
            bits = self.a51.get_bits(64)
            chunked_bits = list(utils.chunks(bits, 8))
            chunked_bits = [self.chunk_to_int(chunk) for chunk in chunked_bits]
            plaintext = self.perform_xor(ciphertext, chunked_bits)
            decrypted_messages.append(plaintext)

        return decrypted_messages
