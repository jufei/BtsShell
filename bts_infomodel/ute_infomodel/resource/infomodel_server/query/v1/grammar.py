# -*- coding: utf-8 -*-
"""
:created on: 03-12-2013

:copyright: NSN
:author: Tomasz Kolek
:contact: tomasz.kolek@nsn.com
"""

from pyparsing import Regex, Literal, Or, Optional, OneOrMore, Empty


dist_name = Regex('(((//)|(/))[A-Z_]+-(0|[1-9][0-9]*|\*))+')('dist_name')
is_part = Literal('is')

predicate_name = OneOrMore(Regex('[^=, >, \], \[, \,, <, <=, >=, !=]+') +
                           Optional(Regex("\[(0|[1-9][0-9]*|\*|\?)\]"))).setParseAction(lambda x: ''.join(x))('name')

predicate_without_quotes = Regex('[^=, >, \], \[, \,, <, <=, >=, !=, "]+')('value')
predicate_with_quotes = Literal('"') + OneOrMore(Regex('[^"]+')).setParseAction(lambda x: ' '.join(x))('value') + Literal('"')
predicate_value = (predicate_without_quotes | predicate_with_quotes)

symbol = Or((Literal("=regex"), Literal('>'), Literal('<'), Literal('>='), Literal('<='), Literal('='), Literal('!=')))('symbol')
empty_symbol = Literal("=empty")('symbol')
non_empty_symbol = Literal("!=empty")('symbol')
empty_value = Empty().setParseAction(lambda x: "")('value')

predicate_body = predicate_name + (((empty_symbol | non_empty_symbol) + empty_value) | (symbol + predicate_value))

predicate_content = (Optional(Literal(',')) + predicate_body).setResultsName('predicates', True)
predicates = Literal('[') + OneOrMore(predicate_content) + Literal(']')

condition_value = Regex('(0|[1-9][0-9]*)')('value')
condition = (symbol + condition_value)('condition')

every = Literal('every')('function')
count = Literal('count')('function')
get_list = Literal('get list')('function')
get_count = Literal('get count')('function')


class Grammar(object):
    """Base grammar"""
    grammar = None


class DistNameGrammar(Grammar):
    """DistNameGrammar"""
    grammar = dist_name


class DistNameWithPredicateGrammar(Grammar):
    """DistNameWithPredicateGrammar"""
    grammar = DistNameGrammar.grammar + is_part + predicates


class EveryGrammar(Grammar):
    """EveryGrammar"""
    grammar = every + DistNameWithPredicateGrammar.grammar


class CountGrammar(Grammar):
    """CountGrammar"""
    grammar = count + DistNameGrammar.grammar + is_part + Optional(predicates) + condition


class GetListGrammar(Grammar):
    """ GetListGrammar"""
    grammar = get_list + DistNameGrammar.grammar + Optional(is_part + predicates)


class GetCountGrammar(Grammar):
    """ GetCountGrammar"""
    grammar = get_count + DistNameGrammar.grammar + is_part + Optional(predicates)


class InfoModelGrammar(object):
    """InfoModelGrammar"""
    def __init__(self):
        self.grammar = (Regex('^') +
                        Or((DistNameGrammar.grammar,
                            DistNameWithPredicateGrammar.grammar,
                            EveryGrammar.grammar,
                            CountGrammar.grammar,
                            GetListGrammar.grammar,
                            GetCountGrammar.grammar)) +
                        Regex('$'))
