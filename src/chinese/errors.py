#!/usr/bin/env python
# coding: utf-8

# Base
class Error(Exception):
    """Base-class for all exceptions raised by this module."""

# Tokenizer
class InvalidEngineError(Error):
    """Provided tokenizer does not exist."""

# Converter
class InvalidArgumentTypeError(Error):
    """Provided argument's type is wrong."""

class StringLengthError(Error):
    """Provided string's length is invalid."""

# Analizer
class InvalidPlatformError(Error):
    """User's platform is not allowed to do some operations."""

class FileNotFoundError(Error):
    """File not found."""

class InvalidKeyError(Error):
    """Provided key is not in tokens."""