import unittest

from meerkat_nest.util.translate_patient_id import translate


class TranslatePatientIdTest(unittest.TestCase):

    def test_translate_method_exists(self):
        translate('')

    def test_translate_arabic_patient_id(self):
        arabic_input = '٣٢١'
        expected = '321'
        actual = translate(arabic_input)
        self.assertEqual(expected, actual)

    def test_translate_mixed_langueges(self):
        arabic_input = '٣٢١321'
        expected = '321321'
        actual = translate(arabic_input)
        self.assertEqual(expected, actual)
