import enum
import string
import unittest
from crc.crc import Byte, CrcRegister, crc8, is_crc_configruation
from crc.crc import CrcConfiguration, Crc8, Crc16, Crc32, CrcCalculator
from collections import namedtuple


class ByteTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_conversion_to_int(self):
        int_value = 0x01
        byte = Byte(int_value)
        self.assertIsInstance(int(byte), int)
        self.assertEqual(int(byte), int_value)

    def test_is_equal_operator(self):
        for value in range(0, 256):
            self.assertEqual(Byte(value) == Byte(value), True)
            self.assertEqual(Byte(value) == Byte(value + 1), False)

    def test_adding_two_bytes_without_overflow(self):
        lhs = Byte(0x02)
        rhs = Byte(0x10)
        expected_result = Byte(0x12)
        self.assertEqual(lhs + rhs, expected_result)

    def test_adding_an_integer_to_a_byte_without_overflow(self):
        lhs = 0xF0
        rhs = Byte(0x02)
        expected_result = Byte(lhs + int(rhs))
        self.assertEqual(lhs + rhs, expected_result)

    def test_adding_two_bytes_with_overflow(self):
        lhs = Byte(0xFA)
        rhs = Byte(0xFA)
        expected_result = Byte(0xFA + 0xFA)

    def test_adding_an_integer_to_a_byte_with_overflow(self):
        lhs = 0xFA
        rhs = Byte(0xFA)
        expected_result = Byte(lhs + int(rhs))
        self.assertEqual(lhs + rhs, expected_result)
        self.assertEqual(lhs + rhs, expected_result)

    def test_instance_based_add(self):
        lhs = Byte(0x00)
        rhs = Byte(0xFA)
        lhs += rhs
        self.assertEqual(lhs._value, rhs._value)


class CrcConfigurationTest(unittest.TestCase):

    def setUp(self):
        self.width = 8
        self.polynom = 0x07
        self.init_value = 0xFF
        self.final_xor_value = 0xAA
        self.reverse_input = True
        self.reverse_output = True

    def test_init_using_defaults(self):
        configuration = CrcConfiguration(self.width, self.polynom)
        self.assertEqual(configuration.width, self.width)
        self.assertEqual(configuration.polynom, self.polynom)
        self.assertEqual(configuration.init_value, 0)
        self.assertEqual(configuration.final_xor_value, 0)
        self.assertEqual(configuration.reverse_input, False)
        self.assertEqual(configuration.reverse_output, False)

    def test_init(self):
        configuration = CrcConfiguration(self.width,
                                         self.polynom,
                                         self.init_value,
                                         self.final_xor_value,
                                         self.reverse_input,
                                         self.reverse_output)

        self.assertEqual(configuration.width, self.width)
        self.assertEqual(configuration.polynom, self.polynom)
        self.assertEqual(configuration.init_value, self.init_value)
        self.assertEqual(configuration.final_xor_value, self.final_xor_value)
        self.assertEqual(configuration.reverse_input, self.reverse_input)
        self.assertEqual(configuration.reverse_output, self.reverse_output)


class CrcModuleTest(unittest.TestCase):

    def test_if_is_crc_configuration_returns_true_for_crc_configuration(self):
        configurations = [CrcConfiguration(0,0), Crc8.CCITT, Crc8.SAEJ1850]
        for configuration in configurations:
            self.assertTrue(is_crc_configruation(configuration))

    def test_if_is_crc_configuration_returns_false_for_none_crc_configuration(self):
        configurations = [None, object(), "stuff", {}]
        for configuration in configurations:
            self.assertFalse(is_crc_configruation(configuration))


class CrcRegisterTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_init_works_with_enum(self):
        config = Crc8.CCITT
        crc_register = CrcRegister(config)



class Crc8Test(unittest.TestCase):

    def setUp(self):
        CrcTestData = namedtuple('CrcTestData', 'data checksum')
        self.crc8_test_suit = [
            CrcTestData(data='', checksum=0x00),
            CrcTestData(data=string.digits[1:], checksum=0xF4),
            CrcTestData(data=string.digits[1:][::-1], checksum=0x91),
            CrcTestData(data=string.digits, checksum=0x45),
            CrcTestData(data=string.digits[::-1], checksum=0x6E),
        ]

    def test_crc8_smoke_test(self):
        data = string.digits[1:]
        expected = 0xF4
        checksum = crc8(data)
        self.assertEqual(checksum, expected)

    def test_crc8_test_suit(self):
        calculator = CrcCalculator(Crc8.CCITT)
        for test in self.crc8_test_suit:
            self.assertEqual(calculator.calculate_checksum(test.data.encode('utf-8')), test.checksum)

class Crc16Test(unittest.TestCase):
    pass

class Crc32Test(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()