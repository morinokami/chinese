from setuptools import setup, find_packages

with open('docs/README-rst') as f:
    desc = f.read()

setup(
    name='chinese',
    version='0.1.0',
    license='MIT',
    url='https://github.com/morinokami/chinese',
    keywords=['Chinese', 'text analysis'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description='Chinese text analyzer',
    long_description = desc,

    author='Shinya Fujino',
    author_email='shf0811@gmail.com',

    packages=find_packages(where='src'),
    package_dir={'chinese': 'src/chinese'},
    package_data={'chinese': ['data/cedict_ts.u8', 'data/dict.txt.big']},
    include_package_data=True,

    install_requires=['jieba', 'pynlpir'],
)
