#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import platform
import re
import subprocess

from chinese.converter import Converter
from chinese.dictionary import Dictionary
from chinese.tokenizer import Tokenizer
import chinese.errors as errors


class ChineseAnalyzer:

    def __init__(self):
        self.dictionary = Dictionary()
        self.dictionary.load()
        self.converter = Converter()
        self.tokenizer = Tokenizer()

    def parse(self, string, *, traditional=False, using=Tokenizer.jieba, dictionary=None):
        """Returns a ChineseAnalyzerResult object.

        Args:
            string (str): A Chinese text.
            traditional (bool): If set to True, the string will be parsed as a Traditional
                Chinese text.
            using: An Engine object or a custom tokenizer derived from TokenizerInterface.
            dictionary (str): A path to your dictionary file.
        """
        tokens = self.tokenizer.tokenize(string, traditional=traditional, using=using)
        if dictionary is not None:
            self.dictionary.load(dictionary)
        if traditional:
            lookup = self.dictionary.lookup_with_traditional_chinese
        else:
            lookup = self.dictionary.lookup_with_simplified_chinese
        parsed_tokens = map(lookup, (token[0] for token in tokens))
        parsed_string = list(zip(tokens, parsed_tokens))
        return ChineseAnalyzerResult(self, tokens, parsed_string, traditional)

class ChineseAnalyzerResult:
    
    def __init__(self, parent, tokens, parsed_string, traditional):
        self.__parent = parent
        self.__tokens = tokens
        self.__parsed_string = parsed_string
        self.__traditional = traditional

    def original(self):
        """Returns the provided string as is."""
        return ''.join(token[0] for token in self.__tokens)

    def tokens(self, *, details=False, unique=False):
        """Returns tokens in the provided text.

        Args:
            details (bool): If set to True, the details of tokens are also returned.
            The content in a detail depends on the tokenizer used.
            unique (bool): If set to True, a unique collection of tokens is returned.
        
        Returns:
            A list of tokens are returned by defulat. If details is set to True,
            a list of tuples containing tokens and their details are returned.
        """
        result = [token for token in self.__tokens] if details else [token[0] for token in self.__tokens]
        if unique:
            from collections import OrderedDict
            result = list(OrderedDict.fromkeys(result))
        
        return result
    
    def freq(self):
        """Returns a Counter object that counts the number of occurrences for each token."""
        from collections import Counter
        return Counter(self.tokens())

    def paragraphs(self):
        """Returns a list of paragraphs in a provided text."""
        delimeter = '\n'
        
        naive_strip_result = self.original().split(delimeter)
        paragraphs_cleaned = [paragraph.strip() for paragraph in naive_strip_result if paragraph]

        return paragraphs_cleaned

    def sentences(self):
        """Returns a list of sentences in a provided text."""
        result = []
        delimiters = re.compile('[。？！；]')
        paragraphs = self.paragraphs()
        
        for paragraph in paragraphs:
            result += [sentence for sentence in delimiters.split(paragraph) if sentence]
        
        return result
    
    def search(self, string):
        """Returns a list of sentences containing the argument string."""
        return [sentence for sentence in self.sentences() if string in sentence]

    def pinyin(self, *, force=False, all_readings=False):
        """Returns a pinyin representation of the provided text.

        Args:
            force (bool): If set to False, tokens that are not in the dictionary are
                not converted to pinyin. If set to True, it tries to convert
                all tokens into a pinyin form.
            all_readings (bool): If set to True, tokens that have multiple readings
                like '那' are converted into the form '[xxx|yyy|zzz]'.

        Returns:
            A string of pinyins which derived from the provided text.
        """
        pinyin_list = self.__pinyin_list(force)
        joined = self.__join(pinyin_list, all_readings)
        cleaned = self.__clean(joined)
        return cleaned

    def __pinyin_list(self, force):
        """Returns a list of lists of pinyins derived from the provided text.
        
        Returns:
            A list of pinyins like [['wǒ'], ['shì'], ['Rìběnrén']]. If some tokens have
            several readings, the corresponding list looks like ['de', 'dī', 'dí', 'dì'].
        """
        lists = []
        converter = self.__parent.converter.prettify
        if self.__traditional:
            lookup_pinyin = self.__parent.dictionary.lookup_pinyin_with_traditional_chinese
        else:
            lookup_pinyin = self.__parent.dictionary.lookup_pinyin_with_simplified_chinese
        
        for parsed in self.__parsed_string:
            lookup_results = parsed[1]
            pinyins = []
            
            for result in lookup_results:
                if result is None:
                    continue

                if result.pinyin is not None:
                    pinyins.append(''.join(converter(ugly_pinyin) for ugly_pinyin in result.pinyin))
                else:
                    if force:
                        joined = ''.join(lookup_pinyin(char) for char in result.match)
                        pinyins.append(joined)
                    else:
                        pinyins.append(result.match)
            
            lists.append(pinyins)
        
        return lists
    
    def __join(self, pinyin_list, all_readings=False):
        def remove_duplicates_from_list(l):
            from collections import OrderedDict
            return list(OrderedDict.fromkeys(l))

        result = []
        for pinyins in pinyin_list:
            if all_readings:
                pinyins = remove_duplicates_from_list(pinyins)
                pinyin = '[{}]'.format('|'.join(pinyins)) if len(pinyins) > 1 else pinyins[0]
                result.append(' ' + pinyin)
            else:
                result.append(' ' + pinyins[0]) # Use the first one: MUST BE FIXED
        return ''.join(result).strip()
    
    def __clean(self, string):
        # zh: ～！¥（）「」【】、：；“‘《》，。？／
        # en: ~!$(){}[],:;"'<>,.?/
        replacers = [
            (' ～', '~'), (' ！', '!'), (' ¥', '$'),
            ('（ ', '('), (' ）', ')'), ('「 ', '{'),
            (' 」', '}'), ('【 ', '['), (' 】', ']'),
            (' 、', ','), (' ：', ':'), (' ；', ';'),
            ('“', '"'), ('‘', '\''), ('《 ', '<'),
            (' 》', '>'), (' ，', ','), (' 。', '.'),
            (' ？', '?'), (' ／ ', '/'),
        ]

        for replacer in replacers:
            string = string.replace(*replacer)
        
        return string
    
    def say(self, *, out=None):
        """Converts the provided text to Chinese audible speech.

        Args:
            out (string): The path for an audio file to be written.

        NOTE: This method utilizes the say command in macOS. It raises
            an error if the platform is not macOS.
        """
        if platform.system() != 'Darwin':
            raise errors.InvalidPlatformError('say can be used only on Mac.')
        elif not Path('/usr/bin/say').exists:
            raise errors.FileNotFoundError('say command is not installed on your machine.')

        voice = 'Mei-Jia' if self.__traditional else 'Ting-Ting'
        command = ['say', '-v', voice, self.original()]
        if out is not None:
            command += ['-o', out]

        subprocess.run(command)
    
    def pformat(self):
        from pprint import pformat
        
        data = {
            'original': self.original(),
            'parsed': [{
                'token': parsed[0],
                'dict_data': [eval(str(d)) for d in parsed[1]]
            } for parsed in self.__parsed_string]
        }
        
        return pformat(data)
    
    def pprint(self):
        """Prints a formatted description of the object."""
        print(self.pformat())

    def __len__(self):
        """Returns the number of tokens in the provided text."""
        return len(self.__tokens)

    def __contains__(self, key):
        """Returns whether the key is in the tokens or not."""
        return any(key == token[0] for token in self.__tokens)

    def __getitem__(self, key):
        """Returns a list of lookup results."""
        if key not in self.tokens():
            raise errors.InvalidKeyError('InvalidKeyError: {}'.format(key))
        for token, dict_data in self.__parsed_string:
            if key == token[0]:
                return dict_data

    def __str__(self):
        from pprint import pformat
        data = {parsed[0][0]: [eval(str(d)) for d in parsed[1]] for parsed in self.__parsed_string}
        return pformat(data)
