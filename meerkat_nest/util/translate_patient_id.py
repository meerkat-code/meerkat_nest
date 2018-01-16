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

arabic_pattern = re.compile("^[٠١٢٣٤٥٦٧٨٩]+$")


def translate(arabic_patient_id):
    if not arabic_patient_id:
        return arabic_patient_id
    result = ''
    for char in arabic_patient_id:
        # if char is not arabic we'd like to return original char
        result += arabic_to_latin_digits_map.get(char, char)
    return result


