import re
from collections import deque

from syllabifier import syllabifyARPA

from english_to_katakana.resource import consonant_to_katakana, cv_to_katakana, vowel_to_katakana


def is_consonant(phone: str) -> bool:
    return phone in [
        'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S', 'SH',
        'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH'
    ]


def is_short_vowel(phone: str) -> bool:
    return phone in ['AE', 'AH', 'IH', 'EH', 'UH']


def is_plosive_or_affricate(phone: str) -> bool:
    return phone in ['B', 'CH', 'D', 'G', 'K', 'P', 'SH', 'T']


def remove_stress(phone: str) -> str:
    return phone.replace('0', '').replace('1', '').replace('2', '')


def syllable_to_katakana(syllable: str) -> str:
    unprocessed = deque()
    output = ''
    phones = syllable.split(' ')
    for (i, phone) in enumerate(phones):
        phone_without_stress = remove_stress(phone)
        if is_consonant(phone_without_stress):
            if len(unprocessed) == 0:
                unprocessed.append(phone)
            else:
                prev_phone = unprocessed.pop()
                prev_phone_without_stress = remove_stress(prev_phone)
                if is_consonant(prev_phone_without_stress):
                    output += consonant_to_katakana[prev_phone_without_stress]
                    unprocessed.append(phone)
                elif prev_phone_without_stress in ['AA', 'AO'] and phone == 'R':
                    pass
                else:
                    unprocessed.append(phone)
        else:
            if len(unprocessed) == 0:
                output += vowel_to_katakana[phone_without_stress]
            else:
                is_stressed = '1' in phone

                prev_phone = unprocessed.pop()
                prev_phone_without_stress = remove_stress(prev_phone)
                if (prev_phone, phone) == ('K', 'AE1'):
                    output += 'キャ'
                else:
                    katakana = cv_to_katakana[f'{prev_phone_without_stress} {phone_without_stress}']
                    output += katakana
                if (
                    is_stressed
                    and is_short_vowel(phone_without_stress)
                    and i < len(phones) - 1
                    and is_plosive_or_affricate(phones[i + 1])
                ):
                    output += 'ッ'
                if phone_without_stress in ['AA', 'AO']:
                    unprocessed.append(phone)

    final = ''
    while len(unprocessed) > 0:
        rest_phone = unprocessed.pop()
        rest_phone_without_stress = remove_stress(rest_phone)
        if rest_phone_without_stress in ['AA', 'AO']:
            continue
        katakana = consonant_to_katakana[rest_phone_without_stress] \
            if is_consonant(rest_phone_without_stress) \
            else vowel_to_katakana[rest_phone_without_stress]
        final = katakana + final
    return output + final


def normalize_m_bilabial_plosive_combination(w: str) -> str:
    pattern = r'ム(バ|ビ|ブ|ベ|ボ|パ|ピ|プ|ペ|ポ)'
    return re.sub(pattern, r'ン\1', w)


def word_to_katakana(w: str, en_dict: dict[str, list[list[str]]]) -> str:
    pronunciation = en_dict[w.lower()][0]
    syllables = syllabifyARPA(pronunciation, silence_warnings=True)
    katakanas = [syllable_to_katakana(syllable) for syllable in syllables]
    if (katakanas[-1] == 'シャン') and (w.endswith('tion')):
        result = ''.join(katakanas[:-1]) + 'ション'
    elif (katakanas[-1] == 'バル') and (w.endswith('ble')):
        result = ''.join(katakanas[:-1]) + 'ブル'
    else:
        result = ''.join(katakanas)
    return normalize_m_bilabial_plosive_combination(result)
