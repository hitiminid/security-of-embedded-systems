def byte_to_bits(byte):
    """
    Function converting int bytes to binary form (represented using str)
    """
    return format(byte, "08b")


def xor(a: str, b: str):
    """
    Perform xor operation on two strings
    """
    return '{0:b}'.format(int(a,2) ^ int(b,2))


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]
