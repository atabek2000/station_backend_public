import re

def cyrillic_to_latin(text):
    cyrillic_to_latin_mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '-', 'ә': 'a', 'і': 'i', 'ң': 'n', 'ғ': 'g'
        , 'ү': 'u', 'ұ': 'u', 'қ': 'q', 'ө': 'o', 'һ': 'h'
    }

    converted_text = ''
    for char in text:
        if char.lower() in cyrillic_to_latin_mapping:
            converted_text += cyrillic_to_latin_mapping[char.lower()]
        else:
            converted_text += re.sub(r"[^0-9A-z]", "", char)

    return converted_text