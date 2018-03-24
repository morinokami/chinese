#!/usr/bin/env python
# coding: utf-8

import pytest

from chinese import ChineseAnalyzer
from chinese.dictionary import Simplified
from chinese.tokenizer import Tokenizer, TokenizerInterface
import chinese.errors as errors

analyzer = ChineseAnalyzer()

@pytest.mark.parametrize('arg, expected',
                         [('你好', '你好'),
                          ('', ''),
                         ])
def test_original(arg, expected):
    result = analyzer.parse(arg)
    assert result.original() == expected

@pytest.mark.parametrize('arg, expected',
                         [('永和服装饰品有限公司', ['永和', '服装', '饰品', '有限公司']),
                          ('', []),
                         ])
def test_tokens(arg, expected):
    result = analyzer.parse(arg)
    assert result.tokens() == expected

@pytest.mark.parametrize('arg, expected',
                         [('我来到北京清华大学', ['我', '来到', '北京', '清华大学']),
                          ('', []),
                         ])
def test_tokens_pynlpir(arg, expected):
    result = analyzer.parse(arg, using=Tokenizer.pynlpir)
    assert result.tokens() == expected

def test_custom_tokenizer_works():
    class MyTokenizer(TokenizerInterface):
        def tokenize(self, string):
            return [('seems',), ('not',), ('working',)]
    my = MyTokenizer()
    result = analyzer.parse('你好', using=my)
    expected = [('seems',), ('not',), ('working',)]
    assert result.tokens(details=True) == expected

def test_invalid_custom_tokenizer_raises():
    class InvalidTokenizer():
        def do_something_awsome(self, x):
            pass
    invalid_tokenizer = InvalidTokenizer()
    
    with pytest.raises(errors.InvalidEngineError) as excinfo:
        analyzer.parse('你好', using=invalid_tokenizer)
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'InvalidEngineError: {}'.format(invalid_tokenizer)

@pytest.mark.parametrize('arg, expected',
                         [('永和服装饰品有限公司', [('永和', 0, 2), ('服装', 2, 4), ('饰品', 4, 6), ('有限公司', 6, 10)]),
                          ('', []),
                         ])
def test_tokens_details(arg, expected):
    result = analyzer.parse(arg)
    assert result.tokens(details=True) == expected

@pytest.mark.parametrize('arg, expected',
                         [('的的的的的在的的的的就以和和和', ['的', '在', '就', '以', '和']),
                          ('', []),
                         ])
def test_tokens_unique(arg, expected):
    result = analyzer.parse(arg)
    assert result.tokens(unique=True) == expected

def test_freq():
    from collections import Counter
    result = analyzer.parse('这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱Python和C++。')
    expected = Counter({'我': 3, '。': 2, '，': 2, '爱': 2, '这是': 1, '一个': 1, '伸手不见五指': 1, '的': 1, '黑夜': 1, '叫': 1, '孙悟空': 1, '北京': 1, 'Python': 1, '和': 1, 'C++': 1})
    assert result.freq() == expected

@pytest.mark.parametrize('arg, expected',
                         [('您好。请问小美在家吗？\n\n在。请稍等。', ['您好。请问小美在家吗？', '在。请稍等。']),
                          ('你好', ['你好']),
                          ('', []),
                         ])
def test_paragraphs(arg, expected):
    result = analyzer.parse(arg)
    assert result.paragraphs() == expected

@pytest.mark.parametrize('arg, expected',
                         [('您好。请问小美在家吗？\n\n在。请稍等。', ['您好', '请问小美在家吗', '在', '请稍等']),
                          ('你好', ['你好']),
                          ('', []),
                         ])
def test_sentences(arg, expected):
    result = analyzer.parse(arg)
    assert result.sentences() == expected

text_for_search = '自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。自然语言处理是一门融语言学、计算机科学、数学于一体的科学。因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，所以它与语言学的研究有着密切的联系，但又有重要的区别。自然语言处理并不是一般地研究自然语言，而在于研制能有效地实现自然语言通信的计算机系统，特别是其中的软件系统。因而它是计算机科学的一部分。'
@pytest.mark.parametrize('arg, expected',
                         [('数学', ['自然语言处理是一门融语言学、计算机科学、数学于一体的科学']),
                          ('小笼包', []),
                         ])
def test_search(arg, expected):
    result = analyzer.parse(text_for_search)
    assert result.search(arg) == expected

@pytest.mark.parametrize('arg, expected, traditional, force, all_readings',
                         [('你叫什么名字？', 'nǐ jiào shénme míngzi?', False, False, False),
                          ('我喜歡這個味道', 'wǒ xǐhuan zhège wèidao', True, False, False),
                          ('', '', False, False, False),
                          ('', '', True, False, False),
                          ('他来到了网易杭研大厦吗？', 'tā láidào le Wǎngyì hángyán dàshà mǎ?', False, True, False),
                          ('这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱Python和C++。', 'zhèshì yīgè shēnshǒubùjiànwǔzhǐ de hēiyè. wǒ jiào SūnWùkōng, wǒ ài Běijīng, wǒ ài Python hé C++.', False, True, False),
                          ('現代漢語漢字大致分成正體字／繁體字與簡體字兩個體系', 'xiàndàihànyǔ hànzì dàzhì fēnchéng zhèngtǐzì/fántǐzì yú jiǎntǐzì liǎnggè tǐxì', True, True, False),
                          ('那是谁的孩子？', '[Nā|Nuó|nǎ|nà|nuó] shì shéi [de|dī|dí|dì] háizi?', False, False, True),
                          ('', '', False, False, True),
                          ('他来到了网易杭研大厦吗？', 'tā láidào [le|liǎo|liào] Wǎngyì hángyán dàshà [mǎ|ma]?', False, True, True),
                          ('这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱Python和C++。', 'zhèshì yīgè shēnshǒubùjiànwǔzhǐ [de|dī|dí|dì] hēiyè. wǒ jiào SūnWùkōng, wǒ ài Běijīng, wǒ ài Python [hé|Hé|hè|hú|huó|huò] C++.', False, True, True),
                         ])
def test_pinyin(arg, expected, traditional, force, all_readings):
    result = analyzer.parse(arg, traditional=traditional)
    assert result.pinyin(force=force, all_readings=all_readings) == expected

def test_pformat1():
    result = analyzer.parse('你叫什么名字？')
    expected = '''{'original': '你叫什么名字？',
 'parsed': [{'dict_data': [{'definitions': ['you (informal, as opposed to '
                                            'courteous 您[nin2])'],
                            'kind': 'Simplified',
                            'match': '你',
                            'pinyin': ['ni3']}],
             'token': ('你', 0, 1)},
            {'dict_data': [{'definitions': ['to shout',
                                            'to call',
                                            'to order',
                                            'to ask',
                                            'to be called',
                                            'by (indicates agent in the '
                                            'passive mood)'],
                            'kind': 'Simplified',
                            'match': '叫',
                            'pinyin': ['jiao4']},
                           {'definitions': ['variant of 叫[jiao4]'],
                            'kind': 'Simplified',
                            'match': '呌',
                            'pinyin': ['jiao4']}],
             'token': ('叫', 1, 2)},
            {'dict_data': [{'definitions': ['what?', 'something', 'anything'],
                            'kind': 'Simplified',
                            'match': '什麼',
                            'pinyin': ['shen2', 'me5']}],
             'token': ('什么', 2, 4)},
            {'dict_data': [{'definitions': ['name (of a person or thing)',
                                            'CL:個|个[ge4]'],
                            'kind': 'Simplified',
                            'match': '名字',
                            'pinyin': ['ming2', 'zi5']}],
             'token': ('名字', 4, 6)},
            {'dict_data': [{'definitions': None,
                            'kind': 'Simplified',
                            'match': '？',
                            'pinyin': None}],
             'token': ('？', 6, 7)}]}'''
    assert result.pformat() == expected

def test_pformat2():
    result = analyzer.parse('')
    expected = '''{'original': '', 'parsed': []}'''
    assert result.pformat() == expected

@pytest.mark.parametrize('arg, expected',
                         [('永和服装饰品有限公司', 4),
                          ('', 0),
                         ])
def test_len(arg, expected):
    result = analyzer.parse(arg)
    assert len(result) == expected

def test_contains():
    result = analyzer.parse('永和服装饰品有限公司')
    assert '有限公司' in result

@pytest.mark.parametrize('arg, token',
                         [('永和服装饰品有限公司', '你好'),
                          ('永和服装饰品有限公司', '公司'),
                         ])
def test_not_contain(arg, token):
    result = analyzer.parse(arg)
    assert token not in result

def test_getitem():
    result = analyzer.parse('永和服装饰品有限公司')
    expected = [Simplified('永和', ['Yong3', 'he2'], ['Yonghe or Yungho city in New Taipei City 新北市[Xin1 bei3 shi4], Taiwan'])]
    assert result['永和'] == expected

@pytest.mark.parametrize('arg, token',
                         [('永和服装饰品有限公司', '你好'),
                          ('永和服装饰品有限公司', '公司'),
                         ])
def test_getitem_raises(arg, token):
    result = analyzer.parse(arg)
    with pytest.raises(errors.InvalidKeyError) as excinfo:
        result[token]
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'InvalidKeyError: {}'.format(token)

def test_str1():
    result = analyzer.parse('你叫什么名字？')
    expected = '''{'什么': [{'definitions': ['what?', 'something', 'anything'],
         'kind': 'Simplified',
         'match': '什麼',
         'pinyin': ['shen2', 'me5']}],
 '你': [{'definitions': ['you (informal, as opposed to courteous 您[nin2])'],
        'kind': 'Simplified',
        'match': '你',
        'pinyin': ['ni3']}],
 '叫': [{'definitions': ['to shout',
                        'to call',
                        'to order',
                        'to ask',
                        'to be called',
                        'by (indicates agent in the passive mood)'],
        'kind': 'Simplified',
        'match': '叫',
        'pinyin': ['jiao4']},
       {'definitions': ['variant of 叫[jiao4]'],
        'kind': 'Simplified',
        'match': '呌',
        'pinyin': ['jiao4']}],
 '名字': [{'definitions': ['name (of a person or thing)', 'CL:個|个[ge4]'],
         'kind': 'Simplified',
         'match': '名字',
         'pinyin': ['ming2', 'zi5']}],
 '？': [{'definitions': None,
        'kind': 'Simplified',
        'match': '？',
        'pinyin': None}]}'''
    assert str(result) == expected

def test_str2():
    result = analyzer.parse('的的的的的在的的的的就以和和和')
    expected = '''{'以': [{'definitions': ['old variant of 以[yi3]'],
        'kind': 'Simplified',
        'match': '㕥',
        'pinyin': ['yi3']},
       {'definitions': ['old variant of 以[yi3]'],
        'kind': 'Simplified',
        'match': '㠯',
        'pinyin': ['yi3']},
       {'definitions': ['abbr. for Israel 以色列[Yi3 se4 lie4]'],
        'kind': 'Simplified',
        'match': '以',
        'pinyin': ['Yi3']},
       {'definitions': ['to use',
                        'by means of',
                        'according to',
                        'in order to',
                        'because of',
                        'at (a certain date or place)'],
        'kind': 'Simplified',
        'match': '以',
        'pinyin': ['yi3']}],
 '和': [{'definitions': ['old variant of 和[he2]'],
        'kind': 'Simplified',
        'match': '咊',
        'pinyin': ['he2']},
       {'definitions': ['surname He', 'Japanese (food, clothes etc)'],
        'kind': 'Simplified',
        'match': '和',
        'pinyin': ['He2']},
       {'definitions': ['and',
                        'together with',
                        'with',
                        'sum',
                        'union',
                        'peace',
                        'harmony',
                        'Taiwan pr. [han4] when it means "and" or "with"'],
        'kind': 'Simplified',
        'match': '和',
        'pinyin': ['he2']},
       {'definitions': ["to compose a poem in reply (to sb's poem) using the "
                        'same rhyme sequence',
                        'to join in the singing',
                        'to chime in with others'],
        'kind': 'Simplified',
        'match': '和',
        'pinyin': ['he4']},
       {'definitions': ['to complete a set in mahjong or playing cards'],
        'kind': 'Simplified',
        'match': '和',
        'pinyin': ['hu2']},
       {'definitions': ['to combine a powdery substance (flour, plaster etc) '
                        'with water',
                        'Taiwan pr. [huo4]'],
        'kind': 'Simplified',
        'match': '和',
        'pinyin': ['huo2']},
       {'definitions': ['to mix (ingredients) together',
                        'to blend',
                        'classifier for rinses of clothes',
                        'classifier for boilings of medicinal herbs'],
        'kind': 'Simplified',
        'match': '和',
        'pinyin': ['huo4']},
       {'definitions': ['old variant of 和[he2]', 'harmonious'],
        'kind': 'Simplified',
        'match': '龢',
        'pinyin': ['he2']}],
 '在': [{'definitions': ['(located) at',
                        '(to be) in',
                        'to exist',
                        'in the middle of doing sth',
                        '(indicating an action in progress)'],
        'kind': 'Simplified',
        'match': '在',
        'pinyin': ['zai4']}],
 '就': [{'definitions': ['at once',
                        'right away',
                        'only',
                        'just (emphasis)',
                        'as early as',
                        'already',
                        'as soon as',
                        'then',
                        'in that case',
                        'as many as',
                        'even if',
                        'to approach',
                        'to move towards',
                        'to undertake',
                        'to engage in',
                        'to suffer',
                        'subjected to',
                        'to accomplish',
                        'to take advantage of',
                        'to go with (of foods)',
                        'with regard to',
                        'concerning'],
        'kind': 'Simplified',
        'match': '就',
        'pinyin': ['jiu4']}],
 '的': [{'definitions': ['of',
                        "~'s (possessive particle)",
                        '(used after an attribute)',
                        '(used to form a nominal expression)',
                        '(used at the end of a declarative sentence for '
                        'emphasis)'],
        'kind': 'Simplified',
        'match': '的',
        'pinyin': ['de5']},
       {'definitions': ['see 的士[di1 shi4]'],
        'kind': 'Simplified',
        'match': '的',
        'pinyin': ['di1']},
       {'definitions': ['really and truly'],
        'kind': 'Simplified',
        'match': '的',
        'pinyin': ['di2']},
       {'definitions': ['aim', 'clear'],
        'kind': 'Simplified',
        'match': '的',
        'pinyin': ['di4']}]}'''
    assert str(result) == expected

def test_str3():
    result = analyzer.parse('')
    expected = '{}'
    assert str(result) == expected