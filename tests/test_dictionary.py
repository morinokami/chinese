#!/usr/bin/env python
# coding: utf-8

import pytest

from chinese.dictionary import Dictionary, Traditional, Simplified
import chinese.errors as errors

dictionary = Dictionary()

# Parser


# CEDICT

## lookup

def test_lookup_with_simplified_chinese():
    result = dictionary.lookup_with_simplified_chinese('爱')
    expected = [Simplified('愛', ['ai4'], ['to love', 'to be fond of', 'to like', 'affection', 'to be inclined (to do sth)', 'to tend to (happen)'])]
    assert result == expected

def test_lookup_with_simplified_chinese_two_characters():
    result = dictionary.lookup_with_simplified_chinese('宝贝')
    expected = [Simplified('寶貝', ['bao3', 'bei4'], ['treasured object', 'treasure', 'darling', 'baby', 'cowry', 'good-for-nothing or queer character'])]
    assert result == expected

def test_lookup_with_simplified_chinese_three_characters():
    result = dictionary.lookup_with_simplified_chinese('普通话')
    expected = [Simplified('普通話', ['pu3', 'tong1', 'hua4'], ['Mandarin (common language)', 'Putonghua (common speech of the Chinese language)', 'ordinary speech'])]
    assert result == expected

def test_lookup_with_traditional_chinese():
    result = dictionary.lookup_with_traditional_chinese('馬')
    expected = [Traditional('马', ['Ma3'], ['surname Ma', 'abbr. for Malaysia 馬來西亞|马来西亚[Ma3 lai2 xi1 ya4]']), Traditional('马', ['ma3'], ['horse', 'CL:匹[pi3]', 'horse or cavalry piece in Chinese chess', 'knight in Western chess'])]
    assert result == expected

def test_lookup_with_traditional_chinese_two_characters():
    result = dictionary.lookup_with_traditional_chinese('中國')
    expected = [Traditional('中国', ['Zhong1', 'guo2'], ['China'])]
    assert result == expected

def test_lookup_with_traditional_chinese_three_characters():
    result = dictionary.lookup_with_traditional_chinese('繁體字')
    expected = [Traditional('繁体字', ['fan2', 'ti3', 'zi4'], ['traditional Chinese character'])]
    assert result == expected

def test_lookup_with_non_chinese_character_simplified():
    result = dictionary.lookup_with_simplified_chinese('？')
    expected = [Simplified('？', None, None)]
    assert result == expected

def test_lookup_with_non_chinese_character_traditional():
    result = dictionary.lookup_with_traditional_chinese('？')
    expected = [Traditional('？', None, None)]
    assert result == expected

## lookup_pinyin

def test_lookup_pinyin_with_simplified_chinese():
    result = dictionary.lookup_pinyin_with_simplified_chinese('我')
    expected = 'wǒ'
    assert result == expected

def test_lookup_pinyin_with_traditional_chinese():
    result = dictionary.lookup_pinyin_with_traditional_chinese('體')
    expected = 'tǐ'
    assert result == expected

def test_lookup_pinyin_with_non_chinese_character_simplified1():
    result = dictionary.lookup_pinyin_with_simplified_chinese('？')
    expected = '？'
    assert result == expected

def test_lookup_pinyin_with_non_chinese_character_simplified2():
    result = dictionary.lookup_pinyin_with_simplified_chinese('P')
    expected = 'P'
    assert result == expected

def test_lookup_pinyin_with_non_chinese_character_traditional():
    result = dictionary.lookup_pinyin_with_traditional_chinese('？')
    expected = '？'
    assert result == expected

def test_lookup_pinyin_with_simplified_chinese_raises():
    arg = '你好'
    with pytest.raises(errors.StringLengthError) as excinfo:
        dictionary.lookup_pinyin_with_simplified_chinese(arg)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Argument must be a single character: {}'.format(arg)

def test_lookup_pinyin_with_traditional_chinese_raises():
    arg = '繁體字'
    with pytest.raises(errors.StringLengthError) as excinfo:
        dictionary.lookup_pinyin_with_traditional_chinese(arg)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Argument must be a single character: {}'.format(arg)

## lookup_meaning

def test_lookup_meaning_with_simplified_chinese():
    result = dictionary.lookup_meaning_with_simplified_chinese('我')
    expected = ['I', 'me', 'my']
    assert result == expected

def test_lookup_meaning_with_traditional_chinese():
    result = dictionary.lookup_meaning_with_traditional_chinese('體')
    expected = ['body', 'form', 'style', 'system', 'substance', 'to experience', 'aspect (linguistics)']
    assert result == expected

def test_lookup_meaning_with_non_chinese_character_simplified1():
    result = dictionary.lookup_meaning_with_simplified_chinese('？')
    expected = None
    assert result == expected

def test_lookup_meaning_with_non_chinese_character_simplified2():
    result = dictionary.lookup_meaning_with_simplified_chinese('P')
    expected = None
    assert result == expected

def test_lookup_meaning_with_non_chinese_character_traditional():
    result = dictionary.lookup_meaning_with_traditional_chinese('？')
    expected = None
    assert result == expected

def test_lookup_meaning_with_simplified_chinese_raises():
    arg = '你好'
    with pytest.raises(errors.StringLengthError) as excinfo:
        dictionary.lookup_meaning_with_simplified_chinese(arg)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Argument must be a single character: {}'.format(arg)

def test_lookup_meaning_with_traditional_chinese_raises():
    arg = '繁體字'
    with pytest.raises(errors.StringLengthError) as excinfo:
        dictionary.lookup_meaning_with_traditional_chinese(arg)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Argument must be a single character: {}'.format(arg)

## is_chinese_character

def test_is_chinese_character1():
    result = dictionary.is_chinese_character('好')
    assert result

def test_is_chinese_character2():
    result = dictionary.is_chinese_character('あ')
    assert not result
