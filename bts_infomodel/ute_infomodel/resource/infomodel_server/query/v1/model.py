# -*- coding: utf-8 -*-
"""
:created on: 03-12-2013

:copyright: NSN
:author: Tomasz Kolek, Sabat Pawel
:contact: tomasz.kolek@nsn.com, pawel.sabat@nsn.com
"""

import re
from .decorator import query_timeout
from infomodel_server.util import dump_object_to_dict
from infomodel_server.exception import InfoModelObjectParameterNotFoundException, InfoModelObjectIndexedParameterNotFoundException


def _comparator_function(condition_operator):
    """Change string condition operator to callable function."""
    comparators = {
        '>': lambda x, y: x > y,
        '>=': lambda x, y: x >= y,
        '<': lambda x, y: x < y,
        '<=': lambda x, y: x <= y,
        '=': lambda x, y: x == y,
        '!=': lambda x, y: x != y,
        '=regex': lambda x, y: True if re.match(str(y), str(x)) else False,
        '=empty': lambda x, y: not x and x != 0,
        '!=empty': lambda x, y: x or x == 0,
    }

    return comparators[condition_operator]


def _filter_dump_objects(dump_objects_map, dist_name_regex):
    """Filter dump_object_map by dist_name_regex."""
    compiled_filter = re.compile(dist_name_regex)
    filtered_dump_objects = []
    dump_objects_map_iterator = dump_objects_map.entrySet().iterator()
    while dump_objects_map_iterator.hasNext():
        entry = dump_objects_map_iterator.next()
        if compiled_filter.search(entry.getKey().getDistName()):
            filtered_dump_objects.append((entry.getKey().getDistName(), entry.getValue()))
    return filtered_dump_objects


def _extract_location_parts(location):
    return [re.match(r'(?P<part>[^\[,\]]*)(\[(?P<index>.*)\])*', part).groups()[::2] for part in location.split('.')]


def _get_objects_amount(dump_dict_objects, predicates):
    return len([True for _, dump_object in dump_dict_objects if _check_object(dump_object, predicates)])


def _check_objects_count(dump_dict_objects, predicates, condition_operator, condition_value):
    """check_objects_count"""
    counter = _get_objects_amount(dump_dict_objects, predicates)
    comparator = _comparator_function(condition_operator)
    return comparator(counter, condition_value)


def _check_object(dump_dict_object, predicates):
    """check_object"""
    for name, symbol, expected_value in predicates:
        location_parts = _extract_location_parts(name)
        comp = _comparator_function(symbol)
        if not _check_value(location_parts, dump_dict_object, expected_value, comp):
            return False
    return True


def _check_values_in_list(names, source, expected_value, comp, index, depth):
    depth += 1
    if index == "*":
        return all(_check_value(names, s, expected_value, comp, depth) for s in source)
    elif index == "?":
        return any(_check_value(names, s, expected_value, comp, depth) for s in source)
    elif unicode(index).isnumeric():
        value = _check_value(names, source[int(index)], expected_value, comp, depth)
    else:
        value = comp(source, expected_value)

    return value


def _check_values_depending_on_type(names, source, expected_value, comp, index, depth):
    if isinstance(source, list):
        return _check_values_in_list(names, source, expected_value, comp, index, depth)
    elif isinstance(source, dict):
        depth += 1
        return _check_value(names, source, expected_value, comp, depth)
    else:
        return comp(source, expected_value)


def _check_value(names, source, expected_value, comp, depth=0):
    if depth == len(names):
        return comp(source, expected_value)
    name, index = names[depth]
    try:
        source = source[name]
        return _check_values_depending_on_type(names, source, expected_value, comp, index, depth)
    except IndexError:
        raise InfoModelObjectIndexedParameterNotFoundException('InfoModel object parameter: `{}` with index {} not found.'.format(name, index))
    except (KeyError, TypeError):
        raise InfoModelObjectParameterNotFoundException('InfoModel object parameter: `{}` not found.'.format(name))


def _check_every_object(dump_dict_objects, predicates):
    """check_every_object"""
    for _, dump_object in dump_dict_objects:
        if not _check_object(dump_object, predicates):
            return False
    return len(dump_dict_objects) > 0


def _check_any_object(dump_dict_objects, predicates):
    """check_any_object"""
    for _, dump_dict_object in dump_dict_objects:
        if _check_object(dump_dict_object, predicates):
            return True
    return False


def _get_filtered_objects_list(dump_dict_objects, predicates):
    return [(dist_name, dump_dict_object) for dist_name, dump_dict_object in dump_dict_objects if _check_object(dump_dict_object, predicates)]


class Query(object):
    def __init__(self, expression, parameters):
        self.expression = expression
        self.parameters = parameters


class QueryModel(object):
    def __init__(self, model):
        self.model = model

    def _query(self, dist_name_regex, timeout):
        dump_objects_map = self.model.get_dump_objects_map(timeout)
        filtered_dump_objects = _filter_dump_objects(dump_objects_map, dist_name_regex)
        dump_dict_objects = [(dist_name, dump_object_to_dict(dump_object)) for dist_name, dump_object in filtered_dump_objects]
        return dump_dict_objects

    @query_timeout
    def query_count(self, query, timeout):
        """Logic for query count expression."""
        dist_name_regex = query.parameters['dist_name']
        predicates = query.parameters['predicates']
        condition_operator = query.parameters['condition_symbol']
        condition_value = query.parameters['condition_value']
        dump_dict_objects = self._query(dist_name_regex, timeout)
        return _check_objects_count(dump_dict_objects, predicates, condition_operator, condition_value)

    @query_timeout
    def query_every(self, query, timeout):
        """Logic for query every expression."""
        dist_name_regex, predicates = query.parameters['dist_name'], query.parameters['predicates']
        dump_dict_objects = self._query(dist_name_regex, timeout)
        return _check_every_object(dump_dict_objects, predicates)

    @query_timeout
    def query_check(self, query, timeout):
        """Logic for query check expression."""
        dist_name_regex, predicates = query.parameters['dist_name'], query.parameters['predicates']
        dump_dict_objects = self._query(dist_name_regex, timeout)
        return _check_any_object(dump_dict_objects, predicates)

    @query_timeout
    def query_get_list(self, query, timeout):
        """Logic for query get list expression."""
        dist_name_regex, predicates = query.parameters['dist_name'], query.parameters['predicates']
        dump_dict_objects = self._query(dist_name_regex, timeout)
        return _get_filtered_objects_list(dump_dict_objects, predicates)

    @query_timeout
    def query_get_count(self, query, timeout):
        """Logic for query get count expression."""
        dist_name_regex, predicates = query.parameters['dist_name'], query.parameters['predicates']
        dump_dict_objects = self._query(dist_name_regex, timeout)
        return _get_objects_amount(dump_dict_objects, predicates)
