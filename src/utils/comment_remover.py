#!/usr/bin/env python3
# encoding: utf-8

"""
Remove comments from source files
"""

import re
import tokenize
import sqlparse

from io import StringIO


def python_comments(source):
    """
    Remove comments from python source code
    :param source: python source code string
    :return: comment cleaned python code as string
    """
    return remove_comments_and_docstrings(source)
    # try:
    #     parsed_code = ast.parse(source)
    # except SyntaxError:
    #     return source
    # lines = astunparse.unparse(parsed_code).split('\n')
    # return '\n'.join([line for line in lines if line.lstrip()[:1] not in ("'", '"')])


def java_comments(source):
    """
    Remove comments from java source code
    :param source: java source code string
    :return: comment cleaned java code as string
    """
    reg_java = re.compile("(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)")
    return re.sub(reg_java, "", source)


def sql_comments(source):
    """
    Remove comments from sql source code
    :param source: sql source code string
    :return: comment cleaned sql code as string
    """
    return sqlparse.format(source, strip_comments=True).strip()


def c_style_comments(source):
    """
    Remove comments from C++ source code
    :param source: cpp source code string
    :return: comment cleaned cpp code as string
    """
    return re.sub('//.*?((?<!\\\)\n|$)|/\*.*?\*/', '', source, flags=re.S)


def comment_remover(source, lang):
    """
    Main function that calls other functions based on the programming language
    :param source: source code string
    :param lang: programming language
    :return: Comment cleaned source code as string
    """
    if lang == "py":
        return python_comments(source)
    elif lang == "cpp" or lang == "cs" or lang == "js" or lang == "c":
        return c_style_comments(source)
    elif lang == "sql":
        return sql_comments(source)
    elif lang == "java":
        return java_comments(source)
    else:
        return source


def remove_comments_and_docstrings(source):
    """
    Returns 'source' minus comments and docstrings.
    """
    source = str.strip(source)
    io_obj = StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        ltext = tok[4]
        # The following two conditionals preserve indentation.
        # This is necessary because we're not using tokenize.untokenize()
        # (because it spits out code with copious amounts of oddly-placed
        # whitespace).
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        # Remove comments:
        if token_type == tokenize.COMMENT:
            pass
        # This series of conditionals removes docstrings:
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
        # This is likely a docstring; double-check we're not inside an operator:
                if prev_toktype != tokenize.NEWLINE:
                    # Note regarding NEWLINE vs NL: The tokenize module
                    # differentiates between newlines that start a new statement
                    # and newlines inside of operators such as parens, brackes,
                    # and curly braces.  Newlines inside of operators are
                    # NEWLINE and newlines that start new code are NL.
                    # Catch whole-module docstrings:
                    if start_col > 0:
                        # Unlabelled indentation means we're inside an operator
                        out += token_string
                    # Note regarding the INDENT token: The tokenize module does
                    # not label indentation inside of an operator (parens,
                    # brackets, and curly braces) as actual indentation.
                    # For example:
                    # def foo():
                    #     "The spaces before this docstring are tokenize.INDENT"
                    #     test = [
                    #         "The spaces before this string do not get a token"
                    #     ]
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    return out
