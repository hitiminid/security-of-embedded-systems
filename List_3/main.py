from time import sleep
import cipher
import encoder
import utils
import communication
import pdb

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


def communicate(c, Encoder, Cipher):
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
            msg = decrypt_message(Cipher, msg, frame_nos)

            while (msg[-1] == '\x00'):
                msg = msg[:-1]
            print(msg)


def split_and_pad_data(message):
    chunks = list(utils.chunks(message, 8))
    while len(chunks[-1]) < 8:
        chunks[-1].append(0)
    return chunks


def decrypt_message(Cipher, msg: list, frame_nos):
    msg = list(utils.chunks(msg, 8))
    msg = Cipher.perform_decryption(msg, frame_nos)
    return msg


def main():
    c = communication.Communication("/dev/ttyUSB0")
    iv = perform_IV_exchange(c)
    Cipher = cipher.Cipher(iv)
    Encoder = encoder.Encoder(Cipher)

    while True:
        communicate(c, Encoder, Cipher)

if __name__ == "__main__":
    main()
