from django.test import TestCase
from django.core.exceptions import ValidationError
from utils import validate_cpf


class ValidateCpfTestCase(TestCase):

    def test_valid_cpf(self):
        # Test with a valid CPF number
        self.assertTrue(validate_cpf('964.715.320-16'))

    def test_invalid_length_cpf(self):
        # Test with an invalid CPF number of incorrect length
        with self.assertRaises(ValidationError):
            validate_cpf('123')

    def test_identical_digits_cpf(self):
        # Test with a CPF number with all identical digits
        with self.assertRaises(ValidationError):
            validate_cpf('11111111111')

    def test_incorrect_digit_cpf(self):
        # Test with a CPF number with incorrect verification digits
        with self.assertRaises(ValidationError):
            validate_cpf('964.715.320-36')
