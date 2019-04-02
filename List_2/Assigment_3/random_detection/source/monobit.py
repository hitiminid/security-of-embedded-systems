import utility
import math


def perform_monobit_test(bits: str):
	print(f"BITS\n {bits}")
	conversion_sum = produce_convertion_sum(bits)
	print(f'conversion_sum = {conversion_sum}')
	s_obs = compute_test_statistic(bits, conversion_sum)
	print(f's_obs = {s_obs}')
	p_value = compute_p_value(s_obs)
	print(f'p_value = {p_value}')
	result = is_string_random(p_value)
	print(f'is random = {result}')

def produce_convertion_sum(bits: str):
	"""
	Convert all ones to +1 and zeros to -1 and then compute their sum.
	"""
	conv_sum = 0
	for bit in bits:
		if bit == '0':
			conv_sum = conv_sum - 1
		else: 
			conv_sum = conv_sum + 1 
	return conv_sum


def compute_test_statistic(bits: str, conv_sum: int):
	n = len(bits)
	s_obs = abs(conv_sum) / math.sqrt(n)
	return s_obs

	

def compute_p_value(s_obs):
	p_value = math.erfc(s_obs / math.sqrt(2))
	return p_value


def is_string_random(p_value):
	return True if p_value >= 0.01 else False


# file_path = "/home/pietrek/UCZELNIA/MGR/embedded-security/List_2/Assigment_3/tests/test"
# text = utility.load_text(file_path)
# perform_monobit_test(text)