# -*- coding: utf-8 -*-
"""
:created on: 03.03.14

:copyright: NSN
:author: Bartłomiej Idzikowski
:contact: bartlomiej.idzikowski@nsn.com
"""


from pyparsing import ParseException
from infomodel_server.util import logger as _logger
from infomodel_server.exception import InfoModelQueryExpressionSyntaxException


class InfoModelQueryParser(object):
    def __init__(self, grammar):
        self.grammar = grammar.grammar

    def parse(self, expression):
        """InfoModel query parser."""
        try:
            """Parse expression."""
            parsed = self.grammar.parseString(expression)
            if not parsed.function:
                parsed.function = 'check'
            return parsed
        except ParseException, e:
            _logger.debug(str(e))
            raise InfoModelQueryExpressionSyntaxException("%s in query: '%s'" % (str(e), expression))
