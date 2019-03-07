import unittest
import frequency


class FrequencyTest(unittest.TestCase):

    def test_check_valid_random(self):
        # Arrange
        bits = "1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000"
        M = 10

        # Act
        is_random = frequency.perform_block_frequency_test(bits, M)

        # Assert
        assert is_random

    def test_not_random(self):
        # Arrange
        bits = "111111111111111111"
        M = 3

        # Act
        is_random = frequency.perform_block_frequency_test(bits, M)

        # Assert
        assert not is_random

    def test_divide_input_one_block_string(self):
        # Arrange
        bits = "000"
        M = 3

        # Act
        blocks = frequency.divide_input(bits, M)
        # Assert
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "000")

    def test_divide_input_discard_unused_bits(self):
        # Arrange
        bits = "0001"
        M = 3

        # Act
        blocks = frequency.divide_input(bits, M)

        # Assert
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "000")


if __name__ == '__main__':
    unittest.main()
