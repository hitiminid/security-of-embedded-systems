import utility
import math
import scipy.special as scipy


def perform_block_frequency_test(bits: str, M: int):
    """
    M - length of each block
    """

    blocks = divide_input(bits, M)
    proportion_list = determine_blocks_proportion(blocks, M)
    # print(f"proportion list: {proportion_list}")
    statistic = compute_statistic(proportion_list, M)
    # print(f"statistic: {statistic}")
    p_value = compute_p_value(statistic, M)
    # print(f"p-value: {p_value}")
    return is_string_random(p_value)


def divide_input(bits: str, M: int):

    blocks = [bits[i:i + M] for i in range(0, len(bits), M)]

    if len(blocks) >= 2:
        if len(blocks[-2]) != len(blocks[-1]):
            del blocks[-1]

    return blocks


def determine_blocks_proportion(blocks, M):
    proportion_list = [determine_proportion(block, M) for block in blocks]
    return proportion_list


def determine_proportion(block, M: int):
    number_of_ones = block.count('1')
    return number_of_ones / M


def compute_statistic(proportion_list, M):
    elements = [(proportion - .5)**2 for proportion in proportion_list]
    modified_proportions_sum = sum(elements)
    return 4 * M * modified_proportions_sum


def compute_p_value(statistic, M):
    return 1 - scipy.gammainc(M / 2, statistic / 2)


def is_string_random(p_value):
    return True if p_value >= 0.01 else False


# file_path = "/home/pietrek/UCZELNIA/MGR/embedded-security/List_2/Assigment_3/random_detection/test"
# text = utility.load_text(file_path)
# result = perform_block_frequency_test(text, 10)
# print(result)
