#!/usr/bin/env python
# coding: utf-8

import pytest

from chinese.converter import Converter
import chinese.errors as errors

converter = Converter()

@pytest.mark.parametrize('arg, expected',
                         [('Zhong1', 'Zhōng'),
                          ('xiong2', 'xióng'),
                          ('bao3', 'bǎo'),
                          ('e4', 'è'),
                          ('ma5', 'ma'),
                          ('', ''),
                         ])
def test_prettify(arg, expected):
    pinyin = converter.prettify(arg)
    assert pinyin == expected

def test_prettify_raises_type_error():
    arg = 0
    with pytest.raises(errors.InvalidArgumentTypeError) as excinfo:
        converter.prettify(arg)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Argument must be a string: {}'.format(arg)

@pytest.mark.parametrize('arg, expected',
                         [('Zhōng', 'Zhong1'),
                          ('xióng', 'xiong2'),
                          ('bǎo', 'bao3'),
                          ('è', 'e4'),
                          ('ma', 'ma5'),
                          ('', ''),
                         ])
def test_uglify(arg, expected):
    pinyin_uglified = converter.uglify(arg)
    assert pinyin_uglified == expected

def test_uglify_raises_type_error():
    arg = 0
    with pytest.raises(errors.InvalidArgumentTypeError) as excinfo:
        converter.uglify(arg)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'Argument must be a string: {}'.format(arg)