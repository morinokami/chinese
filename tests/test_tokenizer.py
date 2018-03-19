#!/usr/bin/env python
# coding: utf-8

from chinese.tokenizer import Tokenizer

tokenizer = Tokenizer()

def test_tokenize1():
    result = tokenizer.tokenize('永和服装饰品有限公司')
    expected = [('永和', 0, 2), ('服装', 2, 4), ('饰品', 4, 6), ('有限公司', 6, 10)]
    assert result == expected

def test_tokenize2():
    result = tokenizer.tokenize('我来到北京清华大学')
    expected = [('我', 0, 1), ('来到', 1, 3), ('北京', 3, 5), ('清华大学', 5, 9)]
    assert result == expected

def test_tokenize_pynlpir():
    result = tokenizer.tokenize('我来到北京清华大学', engine=tokenizer.Engine.pynlpir)
    expected = [('我', 'pronoun'), ('来到', 'verb'), ('北京', 'noun'), ('清华大学', 'noun')]
    assert result == expected

def test_tokenize_with_other_language():
    result = tokenizer.tokenize('こんにちは')
    expected = [('こ', 0, 1), ('ん', 1, 2), ('に', 2, 3), ('ち', 3, 4), ('は', 4, 5)]
    assert result == expected

def test_tokenize_pynlpir_with_other_language():
    result = tokenizer.tokenize('こんにちは', engine=tokenizer.Engine.pynlpir)
    expected = [('こ', 'noun'), ('ん', 'noun'), ('に', 'noun'), ('ち', 'noun'), ('は', 'noun')]
    assert result == expected

def test_tokenize_with_empty_string():
    result = tokenizer.tokenize('')
    expected = []
    assert result == expected

def test_tokenize_pynlpir_with_empty_string():
    result = tokenizer.tokenize('', engine=tokenizer.Engine.pynlpir)
    expected = []
    assert result == expected

def test_tokenize_with_non_chinese_character():
    result = tokenizer.tokenize('？')
    expected = [('？', 0, 1)]
    assert result == expected

def test_tokenize_pynlpir_with_non_chinese_character():
    result = tokenizer.tokenize('？', engine=tokenizer.Engine.pynlpir)
    expected = [('？', 'punctuation mark')]
    assert result == expected