import pdb
from collections import Counter

class LFSR:  # TODO: probably should be reversed

    def __init__(self, length: int, IV: list, voting_bit_position: int,
                 xoring_bits: list):  # TODO: maybe erase length ???
        self.length = length
        self.IV = IV
        self.bits = IV
        self.voting_bit_position = voting_bit_position
        self.xoring_bits = xoring_bits

    def state(self):
        return self.bits

    def out(self):
        return self.bits[len(self.bits)-1]

    def vote(self):
        return self.bits[self.voting_bit_position]

    def shift(self):
        x = len(self.bits)
        self.bits[1:x] = self.bits[0:x-1]
        R = self.bits[self.xoring_bits[0]]

        for bit in self.xoring_bits[1:]:
            R ^= self.bits[bit-1]
        self.bits[0] = R

    def __repr__(self):
        return f"LSFR {self.length} IV: {self.IV}"

    # def __getitem__(self, i):
    #     return self.bits[i]
    #
    # def __setitem__(self, i, value):
    #     self.bits[i] = value
    #
    # def __len__(self):
    #     return len(self.bits)


class A5_1:

    def __init__(self, IV: list):
        xoring_bits_1 = [13, 16, 17, 18]
        xoring_bits_2 = [20, 21]
        xoring_bits_3 = [7, 20, 21, 22]

        self.lfsr_1 = LFSR(19, IV[:19], 8, xoring_bits_1)
        self.lfsr_2 = LFSR(22, IV[19:-24], 10, xoring_bits_2)
        self.lfsr_3 = LFSR(23, IV[-23:], 10, xoring_bits_3)

    def out(self):
        """
        Return xored bits on 0 position of each LFSR.
        """
        return self.lfsr_1.out() ^ self.lfsr_2.out() ^ self.lfsr_3.out()

    def shift(self):

        majority_bit = self.majority_voting()
        
        if majority_bit == self.lfsr_1.vote():
            self.lfsr_1.shift()

        if majority_bit == self.lfsr_2.vote():
            self.lfsr_2.shift()

        if majority_bit == self.lfsr_3.vote():
            self.lfsr_3.shift()

    def majority_voting(self):
        """
        Count the votes and return most common one.
        """
        votes = [self.lfsr_1.vote(), self.lfsr_2.vote(), self.lfsr_3.vote()]
        return Counter(votes).most_common(1)[0][0]

    def run(self, cycles):
        for i in range(cycles):
            self.shift()
            print(f'IV = {self.get_state()}')
        return self.get_state()

    def get_state(self):
        return self.lfsr_1.state() + self.lfsr_2.state() + self.lfsr_3.state()


IV = [1] * 64
a51 = A5_1(IV)
ajwi = a51.run(3)
