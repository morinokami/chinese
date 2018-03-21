#!/usr/bin/env python
# coding: utf-8

import pytest

from chinese.tokenizer import Tokenizer

tokenizer = Tokenizer()

@pytest.mark.parametrize('arg, expected',
                         [('永和服装饰品有限公司', [('永和', 0, 2), ('服装', 2, 4), ('饰品', 4, 6), ('有限公司', 6, 10)]),
                          ('我来到北京清华大学', [('我', 0, 1), ('来到', 1, 3), ('北京', 3, 5), ('清华大学', 5, 9)]),
                          ('？', [('？', 0, 1)]),
                          ('', []),
                         ])
def test_tokenize(arg, expected):
    result = tokenizer.tokenize(arg)
    assert result == expected

@pytest.mark.parametrize('arg, expected',
                         [('我来到北京清华大学', [('我', 'pronoun'), ('来到', 'verb'), ('北京', 'noun'), ('清华大学', 'noun')]),
                          ('？', [('？', 'punctuation mark')]),
                          ('', []),
                         ])
def test_tokenize_pynlpir(arg, expected):
    result = tokenizer.tokenize(arg, engine=tokenizer.Engine.pynlpir)
    assert result == expected
