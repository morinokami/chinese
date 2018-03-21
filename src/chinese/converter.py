#!/usr/bin/env python
# coding: utf-8

import chinese.errors as errors


class Converter:
    
    toned_vowels = {
        'a': {1: 'ā', 2: 'á', 3: 'ǎ', 4: 'à'},
        'e': {1: 'ē', 2: 'é', 3: 'ě', 4: 'è'},
        'i': {1: 'ī', 2: 'í', 3: 'ǐ', 4: 'ì'},
        'o': {1: 'ō', 2: 'ó', 3: 'ǒ', 4: 'ò'},
        'u': {1: 'ū', 2: 'ú', 3: 'ǔ', 4: 'ù'},
        'A': {1: 'Ā', 2: 'Á', 3: 'Ǎ', 4: 'À'},
        'E': {1: 'Ē', 2: 'É', 3: 'Ě', 4: 'È'},
        'I': {1: 'Ī', 2: 'Í', 3: 'Ǐ', 4: 'Ì'},
        'O': {1: 'Ō', 2: 'Ó', 3: 'Ǒ', 4: 'Ò'},
        'U': {1: 'Ū', 2: 'Ú', 3: 'Ǔ', 4: 'Ù'},
    }
    tones = [1, 2, 3, 4]

    def prettify(self, string):
        if not isinstance(string, str):
            raise errors.InvalidArgumentTypeError('Argument must be a string: {}'.format(string))

        if len(string) == 0 or not string[-1].isdigit():
            return string

        characters, tone = string[:-1], int(string[-1])

        if tone not in self.tones:
            return characters

        if 'a' in characters:
            characters = characters.replace('a', self.toned_vowels['a'][tone])
        elif 'e' in characters:
            characters = characters.replace('e', self.toned_vowels['e'][tone])
        elif 'ou' in characters:
            characters = characters.replace('ou', self.toned_vowels['o'][tone] + 'u')
        else:
            i = len(characters) - 1
            while characters[i] not in self.toned_vowels:
                i -= 1
            vowel = characters[i]
            characters = characters[:i] + self.toned_vowels[vowel][tone] + characters[i+1:]
        
        return characters

    def uglify(self, string):
        if not isinstance(string, str):
            raise errors.InvalidArgumentTypeError('Argument must be a string: {}'.format(string))

        if len(string) == 0:
            return string

        characters, tone = self.__replace_toned_vowel(string)
        return characters + tone

    def __contains_vowel(self, string):
        return any(c.lower() in self.toned_vowels for c in string)

    def __replace_toned_vowel(self, string):
        toned_vowels_decomposed = {
            'ā': ('a', 1), 'á': ('a', 2), 'ǎ': ('a', 3), 'à': ('a', 4),
            'ē': ('e', 1), 'é': ('e', 2), 'ě': ('e', 3), 'è': ('e', 4),
            'ī': ('i', 1), 'í': ('i', 2), 'ǐ': ('i', 3), 'ì': ('i', 4),
            'ō': ('o', 1), 'ó': ('o', 2), 'ǒ': ('o', 3), 'ò': ('o', 4),
            'ū': ('u', 1), 'ú': ('u', 2), 'ǔ': ('u', 3), 'ù': ('u', 4),
            'Ā': ('A', 1), 'Á': ('A', 2), 'Ǎ': ('A', 3), 'À': ('A', 4),
            'Ē': ('E', 1), 'É': ('E', 2), 'Ě': ('E', 3), 'È': ('E', 4),
            'Ī': ('I', 1), 'Í': ('I', 2), 'Ǐ': ('I', 3), 'Ì': ('I', 4),
            'Ō': ('O', 1), 'Ó': ('O', 2), 'Ǒ': ('O', 3), 'Ò': ('O', 4),
            'Ū': ('U', 1), 'Ú': ('U', 2), 'Ǔ': ('U', 3), 'Ù': ('U', 4),
        }

        for c in string:
            if c in toned_vowels_decomposed:
                replacer, tone = toned_vowels_decomposed[c]
                return string.replace(c, replacer), str(tone)
        
        return string, '5'
