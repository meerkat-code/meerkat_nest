import re

latin_to_arabic_digits_map = {
    "0": "٠",
    "1": "١",
    "2": "٢",
    "3": "٣",
    "4": "٤",
    "5": "٥",
    "6": "٦",
    "7": "٧",
    "8": "٨",
    "9": "٩"
}
arabic_to_latin_digits_map = {v: k for k, v in latin_to_arabic_digits_map.items()}

arabic_pattern = re.compile("^[٠١٢٣٤٥٦٧٨٩]{10,10}$")
latin_pattern = re.compile("^[0123456789]{10,10}$")

def translate(arabic_patient_id):
    result = ''
    for char in arabic_patient_id:
        result += arabic_to_latin_digits_map[char]
    return result

#### Tests

import unittest
class TranslatePatientIdTest(unittest.TestCase):

    def test_translate_method_exists(self):
        translate('')

    def test_translate_arabic_patient_id(self):
        arabic_input = '٣٢١'
        expected = '321'
        actual = translate(arabic_input)
        self.assertEqual(expected, actual)
