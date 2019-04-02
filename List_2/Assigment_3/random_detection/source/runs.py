import utility
import math


def perform_runs_test(bits: str):
    # bits = "1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000"
    n = len(bits)
    test_applicable, pi = prerequisite_frequency_test(bits, n)
    
    if test_applicable:
        perform_main_test(bits, n, pi)
    else:
        print('Test not applicable')


def prerequisite_frequency_test(bits, n: int):

    pi = compute_pre_test_proportion(bits)
    tau = compute_tau(n)
    return abs(pi - 0.5) <= tau, pi


def compute_pre_test_proportion(bits: str):
    return bits.count('1') / len(bits)


def compute_tau(n: int):
    tau = 2 / math.sqrt(n)
    return tau


def perform_main_test(bits, n, pi):
    v = compute_test_statistic(bits, n)
    print(f'v: {v}')
    p_value = compute_p_value(v, n, pi)
    print(f'p-value: {p_value}')
    is_random = is_string_random(p_value)
    print(f'is random: {is_random}')


def compute_test_statistic(bits, n: int):
    v = 1

    for bit in range(0, len(bits)-1):
        if bits[bit] != bits[bit + 1]:
            v = v + 1
    return v


def compute_p_value(test_statistic, n, pi):
    numerator = abs(test_statistic - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    inner = numerator / denominator
    return math.erfc(inner)


def is_string_random(p_value, threshold=0.01):  # TODO: move to utility
    return True if p_value >= threshold else False



# file_path = "/home/pietrek/UCZELNIA/MGR/embedded-security/List_2/Assigment_3/random_detection/source/test"
# text = utility.load_text(file_path)
# perform_runs_test(text)
