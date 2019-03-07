import utility
import math


def perform_runs_test(bits: str):
    n = len(bits)
    count = compute_pre_test_proportion(bits)
    print(compute_test_statistic(bits, n))
    # print(count)


def compute_pre_test_proportion(bits: str):
    return bits.count('1') / len(bits)


def compute_test_statistic(bits, n: int):
    return compute_tau(n)


def compute_tau(n: int):
    tau = 2 / math.sqrt(n)
    return tau


def compute_p_value():
    ...


def is_string_random(p_value, threshold=0.01):  # TODO: move to utility
    return True if p_value >= threshold else False


file_path = "/home/pietrek/UCZELNIA/MGR/embedded-security/List_2/Assigment_3/random_detection/test"
text = utility.load_text(file_path)
perform_runs_test(text)
