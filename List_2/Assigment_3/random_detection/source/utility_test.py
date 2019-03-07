import unittest
import utility


class UtilityTest(unittest.TestCase):

    def test_check_valid(self):
        # Arrange
        text = "101"

        # Act
        is_valid = utility.validate_text(text)  # TODO: mock file

        # Assert
        assert is_valid

    def test_invalid_string(self):
        # Arrange
        text = "798dsa"

        # Act
        is_valid = utility.validate_text(text)

        # Assert
        assert not is_valid


if __name__ == '__main__':
    unittest.main()
