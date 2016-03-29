# -*- coding: utf-8 -*-
"""
:created on: 03-12-2013

:copyright: NSN
:author: Tomasz Kolek
:contact: tomasz.kolek@nsn.com
"""

import collections
import Queue
from threading import Thread
from abc import ABCMeta, abstractmethod
from .grammar import InfoModelGrammar
from .model import QueryModel, Query
from .converter import InfoModelConverter
from .parser import InfoModelQueryParser


class Executor(object):

    __metaclass__ = ABCMeta

    def __init__(self, query_model):
        self.query_model = query_model

    @abstractmethod
    def execute(self, params, timeout):
        """Base executor execute method."""


class CountExecutor(Executor):
    def execute(self, query, timeout):
        """Count executor strategy."""
        return self.query_model.query_count(query, timeout)


class CheckExecutor(Executor):
    def execute(self, query, timeout):
        """Check executor strategy."""
        return self.query_model.query_check(query, timeout)


class EveryExecutor(Executor):
    def execute(self, query, timeout):
        """Every executor strategy."""
        return self.query_model.query_every(query, timeout)


class GetListExecutor(Executor):
    def execute(self, query, timeout):
        """Get list executor strategy."""
        return self.query_model.query_get_list(query, timeout)


class GetCountExecutor(Executor):
    def execute(self, query, timeout):
        """Get list executor strategy."""
        return self.query_model.query_get_count(query, timeout)


class QueryExecutor(object):
    EXECUTORS = {
        'check': CheckExecutor,
        'every': EveryExecutor,
        'count': CountExecutor,
        'get list': GetListExecutor,
        'get count': GetCountExecutor,
    }

    def __init__(self, model):
        self.model = model
        self.query_model = QueryModel(self.model)
        self.query_converter = InfoModelConverter()
        self.query_parser = InfoModelQueryParser(InfoModelGrammar())

    def _factory(self, executor_name):
        return QueryExecutor.EXECUTORS[executor_name](self.query_model)

    def execute(self, query, timeout):
        """Execute query on executor."""
        parsed_query = self.query_parser.parse(query)
        converted_query = self.query_converter.convert(parsed_query)
        executor = self._factory(converted_query['function'])
        return executor.execute(query=Query(expression=query, parameters=converted_query), timeout=timeout)

    def _execute_in_thread(self, query, parsed_query, queue, timeout):
        """Execute query on executor."""
        try:
            converted_query = self.query_converter.convert(parsed_query)
            executor = self._factory(converted_query['function'])
            queue.put(executor.execute(query=Query(expression=query, parameters=converted_query), timeout=timeout))
        except Exception, e:
            queue.put(e)
            raise e

    def execute_sequence(self, queries, timeout):
        """Execute queries sequence on executor."""
        queries = collections.OrderedDict(sorted(queries.items()))
        return [self.execute(query, float(timeout)/len(queries)) for _, query in queries.iteritems()]

    def _execute_sequence_in_thread(self, queries, parsed_queries, queue, timeout):
        """Execute queries sequence on executor in thread."""
        try:
            for query_name, query in queries.iteritems():
                converted_query = self.query_converter.convert(parsed_queries[query_name])
                executor = self._factory(converted_query['function'])
                queue.put(executor.execute(query=Query(expression=query, parameters=converted_query), timeout=timeout))
        except Exception, e:
            queue.put(e)
            raise e

    def execute_pararellel(self, queries, timeout):
        """Execute queries pararellel on executor."""
        queue = Queue.Queue()
        threads = [Thread(target=self._execute_in_thread, args=(q, self.query_parser.parse(q), queue, timeout)) for _, q in queries.iteritems()]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout)

        results = []
        while not queue.empty():
            r = queue.get()
            if isinstance(r, Exception):
                raise r
            results.append(r)
        return results

    def _parse_queries(self, queries):
        return {k: self.query_parser.parse(v) for k, v in queries.iteritems()}

    def _collect_results(self, queue):
        results = []
        while not queue.empty():
            r = queue.get()
            if isinstance(r, Exception):
                raise r
            results.append(r)
        return results

    def execute_pararellel_sequences(self, sequences, timeout):
        """Execute sequences in pararellel."""
        queue = Queue.Queue()
        threads = []
        for sequence in sequences.itervalues():
            parsed_queries = self._parse_queries(sequence)
            sequence = collections.OrderedDict(sorted(sequence.items()))
            thread = Thread(target=self._execute_sequence_in_thread, args=(sequence, parsed_queries, queue, float(timeout)/len(sequence)))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout)

        return self._collect_results(queue)
