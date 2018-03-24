#!/usr/bin/env python
# coding: utf-8

import pytest

from chinese.dictionary import Dictionary, Traditional, Simplified
import chinese.errors as errors

dictionary = Dictionary()

# Parser


# CEDICT

## lookup

@pytest.mark.parametrize('arg, expected',
                         [('爱', [Simplified('愛', ['ai4'], ['to love', 'to be fond of', 'to like', 'affection', 'to be inclined (to do sth)', 'to tend to (happen)'])]),
                          ('宝贝', [Simplified('寶貝', ['bao3', 'bei4'], ['treasured object', 'treasure', 'darling', 'baby', 'cowry', 'good-for-nothing or queer character'])]),
                          ('普通话', [Simplified('普通話', ['pu3', 'tong1', 'hua4'], ['Mandarin (common language)', 'Putonghua (common speech of the Chinese language)', 'ordinary speech'])]),
                          ('？', [Simplified('？', None, None)]),
                          ('', []),
                         ])
def test_lookup_with_simplified_chinese(arg, expected):
    result = dictionary.lookup_with_simplified_chinese(arg)
    assert result == expected

@pytest.mark.parametrize('arg, expected',
                         [('馬', [Traditional('马', ['Ma3'], ['surname Ma', 'abbr. for Malaysia 馬來西亞|马来西亚[Ma3 lai2 xi1 ya4]']), Traditional('马', ['ma3'], ['horse', 'CL:匹[pi3]', 'horse or cavalry piece in Chinese chess', 'knight in Western chess'])]),
                          ('中國', [Traditional('中国', ['Zhong1', 'guo2'], ['China'])]),
                          ('繁體字', [Traditional('繁体字', ['fan2', 'ti3', 'zi4'], ['traditional Chinese character'])]),
                          ('？', [Traditional('？', None, None)]),
                          ('', []),
                         ])
def test_lookup_with_traditional_chinese(arg, expected):
    result = dictionary.lookup_with_traditional_chinese(arg)
    assert result == expected

## lookup_pinyin

@pytest.mark.parametrize('arg, expected',
                         [('我', 'wǒ'),
                          ('？', '？'),
                          ('P', 'P'),
                          ('', ''),
                         ])
def test_lookup_pinyin_with_simplified_chinese(arg, expected):
    result = dictionary.lookup_pinyin_with_simplified_chinese(arg)
    assert result == expected

@pytest.mark.parametrize('arg, expected',
                         [('體', 'tǐ'),
                          ('？', '？'),
                          ('P', 'P'),
                          ('', ''),
                         ])
def test_lookup_pinyin_with_traditional_chinese(arg, expected):
    result = dictionary.lookup_pinyin_with_traditional_chinese(arg)
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

@pytest.mark.parametrize('arg, expected',
                         [('我', ['I', 'me', 'my']),
                          ('？', None),
                          ('P', None),
                         ])
def test_lookup_meaning_with_simplified_chinese(arg, expected):
    result = dictionary.lookup_meaning_with_simplified_chinese(arg)
    assert result == expected

@pytest.mark.parametrize('arg, expected',
                         [('體', ['body', 'form', 'style', 'system', 'substance', 'to experience', 'aspect (linguistics)']),
                          ('？', None),
                          ('P', None),
                         ])
def test_lookup_meaning_with_traditional_chinese(arg, expected):
    result = dictionary.lookup_meaning_with_traditional_chinese(arg)
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

@pytest.mark.parametrize('arg, expected',
                         [('好', True),
                          ('あ', False),
                          ('A', False),
                         ])
def test_is_chinese_character(arg, expected):
    result = dictionary.is_chinese_character(arg)
    assert result == expected
