#!/usr/bin/env python
# coding: utf-8

import pytest

from chinese.converter import Converter
import chinese.errors as errors

converter = Converter()

# prettify

def test_prettify_raises_type_error():
    arg = 0
    with pytest.raises(errors.InvalidArgumentTypeError) as excinfo:
        converter.prettify(arg)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Argument must be a string: {}'.format(arg)

def test_prettify_first_tone():
    pinyin = converter.prettify('Zhong1')
    expected = 'Zhōng'
    assert pinyin == expected

def test_prettify_second_tone():
    pinyin = converter.prettify('xiong2')
    expected = 'xióng'
    assert pinyin == expected

def test_prettify_third_tone():
    pinyin = converter.prettify('bao3')
    expected = 'bǎo'
    assert pinyin == expected

def test_prettify_fourth_tone():
    pinyin = converter.prettify('e4')
    expected = 'è'
    assert pinyin == expected

def test_prettify_fifth_tone():
    pinyin = converter.prettify('ma5')
    expected = 'ma'
    assert pinyin == expected

# uglify

def test_uglify_first_tone():
    pinyin_uglified = converter.uglify('Zhōng')
    expected = 'Zhong1'
    assert pinyin_uglified == expected

def test_uglify_second_tone():
    pinyin_uglified = converter.uglify('xióng')
    expected = 'xiong2'
    assert pinyin_uglified == expected

def test_uglify_third_tone():
    pinyin_uglified = converter.uglify('bǎo')
    expected = 'bao3'
    assert pinyin_uglified == expected

def test_uglify_fourth_tone():
    pinyin_uglified = converter.uglify('è')
    expected = 'e4'
    assert pinyin_uglified == expected

def test_uglify_fifth_tone():
    pinyin_uglified = converter.uglify('ma')
    expected = 'ma5'
    assert pinyin_uglified == expected
