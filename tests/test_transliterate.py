import cmudict
import pytest

from english_to_katakana.transliterate import (
    normalize_m_bilabial_plosive_combination,
    syllable_to_katakana,
    word_to_katakana
)


@pytest.fixture(scope='module')
def en_dict() -> dict[str, list[list[str]]]:
    return cmudict.dict()


@pytest.mark.parametrize(
    'syllable, expected',
    [
        pytest.param('F AY1', 'ファイ', id='F AY'),
        pytest.param('N AH0 L', 'ナル', id='N AH L'),
        pytest.param('S T R EH1 NG K TH', 'ストレンクス', id='S T R EH NG K TH'),
        pytest.param('K L AE2', 'クラ', id='K L AE2'),
        pytest.param('K AE1 T', 'キャット', id='K AE1 T'),
        pytest.param('F AE1 T', 'ファット', id='F AE1 T'),
        pytest.param('T R AE0 N', 'トラン', id='T R AE0 N'),
        pytest.param('M ER0', 'マー', id='M ER0'),
    ]
)
def test_syllable_to_katakana(syllable: str, expected: str) -> None:
    assert expected == syllable_to_katakana(syllable)


@pytest.mark.parametrize(
    'syllable, expected',
    [
        pytest.param('final', 'ファイナル', id='final'),
        pytest.param('transformer', 'トランスフォーマー', id='transformer'),
        pytest.param('impossible', 'インパーサブル', id='impossible'),
        pytest.param('hello', 'ハロウ', id='hello'),
        pytest.param('night', 'ナイト', id='night'),
        pytest.param('hot', 'ハート', id='hot'),
        pytest.param('topology', 'トポロジー', id='topology'),
    ]
)
def test_word_to_katakana(
    syllable: str,
    expected: str,
    en_dict: dict[str, list[list[str]]]
) -> None:
    assert expected == word_to_katakana(syllable, en_dict)


@pytest.mark.parametrize(
    'w, expected',
    [
        pytest.param('ナムバー', 'ナンバー', id='number'),
        pytest.param('イムポッシブル', 'インポッシブル', id='impossible'),
    ]
)
def test_normalize_normalize_m_bilabial_plosive_combination(w: str, expected: str) -> str:
    assert expected == normalize_m_bilabial_plosive_combination(w)
