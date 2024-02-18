import re
import sys
from pathlib import Path

import cmudict
from sudachipy import dictionary, tokenizer

from english_to_katakana.transliterate import word_to_katakana


def main() -> None:
    pattern = re.compile('[A-Za-z]+')
    tokenizer_obj = dictionary.Dictionary(dict='full').create()
    mode = tokenizer.Tokenizer.SplitMode.A
    en_dict = cmudict.dict()
    with Path(sys.argv[1]).open(mode='r') as r:
        input_text = r.read()
    sentences = input_text \
        .replace('，', '、') \
        .replace('．', '。') \
        .split('。')
    output_text = ''
    for sentence in sentences:
        results = []
        for morpheme in tokenizer_obj.tokenize(sentence + '。', mode):
            surface = morpheme.surface()
            if re.match(pattern, surface) and surface.lower() in en_dict:
                results.append(word_to_katakana(surface, en_dict))
            else:
                results.append(surface)
        output_text += ''.join(results) + '\n'

    with Path('result.txt').open(mode='w') as w:
        w.write(output_text)
