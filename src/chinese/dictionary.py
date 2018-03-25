#!/usr/bin/env python
# coding: utf-8

from collections import namedtuple
import logging
import os
import pickle
import re

from chinese.converter import Converter
import chinese.errors as errors


logger = logging.getLogger(__name__)

Datum = namedtuple('Datum', ['traditional', 'simplified', 'pinyin', 'definitions'])
Datum.__new__.__defaults__ = (None, None, None, None)

class LookupResult:
    
    def __init__(self, match, pinyin, definitions):
        self.match = match
        self.pinyin = pinyin
        self.definitions = definitions
    
    def __str__(self):
        from pprint import pformat
        
        data = {
            'kind': self.__class__.__name__,
            'match': self.match,
            'pinyin': self.pinyin,
            'definitions': self.definitions
        }

        return pformat(data)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and\
            self.match == other.match and\
            self.pinyin == other.pinyin and\
            self.definitions == other.definitions

class Simplified(LookupResult): pass
class Traditional(LookupResult): pass

class Parser:
    
    @classmethod
    def parse_line(cls, line):
        pattern = r'^(?P<traditional>[^ ]+) (?P<simplified>[^ ]+) \[(?P<pinyin>[\w ]+)\] /(?P<english>.+)/$'
        match = re.match(pattern, line)
        if match:
            return Datum(
                match.group('traditional'),
                match.group('simplified'),
                Parser.__split_pinyin(match.group('pinyin')),
                Parser.__split_english(match.group('english'))
            )
        return Datum()

    @classmethod
    def __split_pinyin(cls, pinyin_string):
        return pinyin_string.split(' ')

    @classmethod
    def __split_english(cls, english_string):
        return english_string.split('/')

class Dictionary:
    
    def __init__(self):
        self.__converter = Converter()
        self.traditional = None
        self.simplified = None

    def __parse_data(self, data):
        traditional = {'name': 'traditional'}
        simplified = {'name': 'simplified'}
        
        for line in data:
            datum = Parser.parse_line(line)
            self.__add_datum(traditional, simplified, datum)
        
        return traditional, simplified
    
    def __add_datum(self, traditional, simplified, datum):
        if datum != Datum():
            traditional_datum = Traditional(
                datum.simplified,
                datum.pinyin,
                datum.definitions,
            )
            simplified_datum = Simplified(
                datum.traditional,
                datum.pinyin,
                datum.definitions,
            )
            if datum.traditional in traditional:
                traditional[datum.traditional].append(traditional_datum)
            else:
                traditional[datum.traditional] = [traditional_datum]
            if datum.simplified in simplified:
                simplified[datum.simplified].append(simplified_datum)
            else:
                simplified[datum.simplified] = [simplified_datum]
    
    def load(self, path=None):
        if path is None:
            logger.info('Loading the default dictionary.')
            directory = os.path.abspath(os.path.dirname(__file__))
            cedict = os.path.join(directory, 'data', 'cedict.pickle')
            with open(cedict, 'rb') as f:
                cedict_data = pickle.load(f)
                self.traditional, self.simplified = cedict_data['traditional'], cedict_data['simplified']
        else:
            with open(path) as f:
                self.traditional, self.simplified = self.__parse_data(f)
    
    def __init_dict_if_necessary(self):
        if self.traditional is None or self.simplified is None:
            self.load()

    def lookup_with_simplified_chinese(self, string):
        self.__init_dict_if_necessary()
        return self.__lookup(self.simplified, string)
    
    def lookup_with_traditional_chinese(self, string):
        self.__init_dict_if_necessary()
        return self.__lookup(self.traditional, string)
    
    def __lookup(self, dictionary, string):
        if len(string) == 0:
            return []
        if string in dictionary:
            return dictionary[string]
        return [Traditional(string, None, None)] if dictionary['name'] == 'traditional' else [Simplified(string, None, None)]
    
    def lookup_pinyin_with_simplified_chinese(self, string):
        self.__init_dict_if_necessary()
        return self.__lookup_pinyin(self.simplified, string)

    def lookup_pinyin_with_traditional_chinese(self, string):
        self.__init_dict_if_necessary()
        return self.__lookup_pinyin(self.traditional, string)
    
    def __lookup_pinyin(self, dictionary, string):
        if len(string) > 1:
            raise errors.StringLengthError('Argument must be a single character: {}'.format(string))
        
        if not self.is_chinese_character(string):
            return string

        if string in dictionary:
            hanzi = dictionary[string][0] # Use the first one: MUST BE FIXED
            return ''.join(map(self.__converter.prettify, hanzi.pinyin)).lower()
        return string

    def lookup_meaning_with_simplified_chinese(self, string):
        self.__init_dict_if_necessary()
        return self.__lookup_meaning(self.simplified, string)

    def lookup_meaning_with_traditional_chinese(self, string):
        self.__init_dict_if_necessary()
        return self.__lookup_meaning(self.traditional, string)
    
    def __lookup_meaning(self, dictionary, string):
        if len(string) > 1:
            raise errors.StringLengthError('Argument must be a single character: {}'.format(string))

        if not self.is_chinese_character(string):
            return None
        
        if string in dictionary:
            hanzi = dictionary[string][0] # Use the first one: MUST BE FIXED
            return hanzi.definitions
        return None
    
    def is_chinese_character(self, string):
        chinese_chars = r'[\u4e00-\u9fff]'
        return re.match(chinese_chars, string) is not None

    def load_raw(self):
        directory = os.path.abspath(os.path.dirname(__file__))
        cedict = os.path.join(directory, 'data', 'cedict_ts.u8')
        with open(cedict) as f:
            self.traditional, self.simplified = self.__parse_data(f)

    def export(self, to):
        data = {
            'simplified': self.simplified,
            'traditional': self.traditional
        }
        with open(to, 'wb') as f:
            pickle.dump(data, f)
