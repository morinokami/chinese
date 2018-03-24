#!/usr/bin/env python
# coding: utf-8

from enum import Enum, auto
import logging
import os

import jieba
import jieba.posseg as pseg
import pynlpir

import chinese.errors as errors

logging.getLogger("jieba").setLevel(logging.WARNING)


class Tokenizer:
    
    class Engine(Enum):
        jieba = auto()
        pynlpir = auto()
    
    def tokenize(self, string, *, traditional=False, engine=Engine.jieba):
        """Returns a list of tokens"""
        if engine == self.Engine.jieba:
            return self.__jieba_tokenize(string, traditional)
        elif engine == self.Engine.pynlpir:
            pynlpir.open()
            return self.__pynlpir_tokenize(string)
        else:
            raise errors.InvalidEngineError('InvalidEngineError: {}'.format(engine))

    def __jieba_tokenize(self, string, traditional):
        if traditional:
            directory = os.path.abspath(os.path.dirname(__file__))
            dict_path = os.path.join(directory, 'data', 'dict.txt.big')
            jieba.set_dictionary(dict_path)
        return list(jieba.tokenize(string))
    
    def __pynlpir_tokenize(self, string):
        if string == '':
            return []
        return pynlpir.segment(string)
