# -*- coding: utf-8 -*-
"""Module for validators

:author: Bartłomiej Idzikowski, Juergen Richter
:contact: bartlomiej.idzikowski@nsn.com, juergen.richter@nsn.com
"""
from re import match
from abc import abstractmethod, ABCMeta
from .exception import EmptyValidatorListError, ValueNotValid
from .result import ValidationResult


class Validator(object):
    """Abstract base validator class."""
    __metaclass__ = ABCMeta

    RESULT_MESSAGE_TEMPLATE = "Validating <%s> with result: <%s>. "

    def __init__(self, *args, **kw):
        self.result_message_template = self.__class__.RESULT_MESSAGE_TEMPLATE

    @abstractmethod
    def validate(self, value, *args, **kw):
        """Abstract method to validating value. All classes inherited from base Validator class.
         have to implement this method.

        :param object value: Value to validate.

        :return: Validation result.
        :rtype: ValidationResult
        """

    def check(self, value, *args, **kw):
        """Check if provided value is valid for specific validator.

        :param object value: Value to validate.
        :raises: ValueNotValid in case when validation result is negative.
        """
        validation_result = self.validate(value, *args, **kw)
        if not validation_result.result:
            raise ValueNotValid(validation_result.message)

    def _build_message(self, *args):
        return self.result_message_template % args


class Assert(Validator):
    """Generic validator which is using function to validate value.

    .. code-block:: python

       validation_expression = Assert(lambda x: isString(x), 'Value is not correct')
       validation_expression.validate('test_string')       # returns ValidationResult object
    """

    def __init__(self, func, err_msg, *args, **kw):
        """
        :param func: Validation function.
        :param string err_msg: Message which will be add when validation fail.
        """
        super(Assert, self).__init__(*args, **kw)
        self.func = func
        self.err_msg = err_msg

    def validate(self, value, *args, **kw):
        """Method checks if specified value meet requirements."""
        result = self.func(value, *args, **kw)
        message = self._build_message(value, result) + (self.err_msg if not result else '')
        return ValidationResult(value, result, message)


class MultiValidator(Validator):
    """Multi validator is base class for validators which contain sub validators."""

    def __init__(self, *args, **kw):
        """Keyword arguments may contain "chain" parameter and it has to be bool. When is missing the False is taken.
           Parameter "chain" is able to limit validation operation by checking if collected results are enough to
           make pass/fail validation decision.
        """
        super(MultiValidator, self).__init__(*args, **kw)
        self.sub_validators = list(args)
        if not self.sub_validators:
            raise EmptyValidatorListError('Validator list is empty')
        self.chain = kw.get('chain', False)

    def _build_message(self, result, results):
        message = ""
        for child in results:
            message += "\n" + "\n".join(map(lambda s: "  %s" % s, str(child).split("\n")))

        message = super(MultiValidator, self)._build_message(result, message)
        return message


class And(MultiValidator):
    """Validator to build validation expression with Validator objects and 'and' operator.

    .. code-block:: python

       validator = And(IsNumber(), InRange(0, 10)
       validator.validate(2)                 # returns True
       validator.validate(11)                # returns False
       validator.validate('test_string_')    # returns False
    """

    RESULT_MESSAGE_TEMPLATE = "Are all of the following conditions fulfilled?: %s%s"

    def __init__(self, *args, **kw):
        """Keyword arguments may contain "chain" parameter and it has to be bool. When is missing the False is taken.
           Parameter "chain" will fail validation after first False result.
        """
        super(And, self).__init__(*args, **kw)

    def _validate(self, value):
        result = True
        results = []
        for v in self.sub_validators:
            r = v.validate(value)
            results.append(r)
            if not r.result:
                result = False
                if self.chain:
                    break
        return result, results

    def validate(self, value, *args, **kw):
        """Method checks if specified value meet requirements."""
        result, results = self._validate(value)
        message = self._build_message(result, results)
        return ValidationResult(value, result, message)


class Or(MultiValidator):
    """Or validator is for build validation expression with Validator objects and 'or' operator.

    .. code-block:: python

       validator = Or(InRange(0, 10), InRange(20, 30))
       print validator.validate(2)   # returns True
       print validator.validate(11)  # returns False
       print validator.validate(25)  # returns True
    """

    RESULT_MESSAGE_TEMPLATE = "Is any of the following conditions fulfilled?: %s%s"

    def __init__(self, *args, **kw):
        """Keyword arguments may contain "chain" parameter and it has to be bool. When is missing the False is taken.
           Parameter "chain" will pass validation after first True result.
        """
        super(Or, self).__init__(*args, **kw)

    def _validate(self, value):
        result = False
        results = []
        for v in self.sub_validators:
            r = v.validate(value)
            results.append(r)
            if not result and r.result:
                result = True
                if self.chain:
                    break

        return result, results

    def validate(self, value, *args, **kw):
        """Method checks if specified value meet requirements."""
        result, results = self._validate(value)
        message = self._build_message(result, results)
        return ValidationResult(value, result, message)


def is_string(value):
    """Function checks if value type is string.

    :param value: Value to validate.
    :return: Validation result.
    :rtype: boolean

    .. code-block:: python

       is_string('example_string')    # returns True
       is_string(10)                  # returns False
    """
    return type(value) in (str, unicode)


class IsString(Validator):
    """Validator is checking that value is string type.

    .. code-block:: python

       validation_expression = IsString()
       validation_expression.validate(10)      # returns ValidationResult object
    """
    RESULT_MESSAGE_TEMPLATE = "Is <%s> a string?: %s"

    def __init__(self, *args, **kw):
        super(IsString, self).__init__(*args, **kw)

    def validate(self, value, *args, **kw):
        """Method checks if specified value meet requirements."""
        result = is_string(value)
        message = self._build_message(value, result)
        return ValidationResult(value, result, message)


def is_ip_address(value):
    """Function checks if value is an IP4 address.

    :param string value: Value to validate.
    :return: Validation result.
    :rtype: boolean

    .. code-block:: python

       is_ip_address('127.0.0.1')          # returns True
       is_ip_address('example_string')     # returns False
    """
    try:
        m = match(r"^(\d+)\.(\d+)\.(\d+)\.(\d+)$", value)
        return m and all(int(byte) < 256 for byte in m.groups())
    except:
        return False


class IsIpAddress(And):
    """Validator is checking that value is an IP4 address.

    .. code-block:: python

       validation_expression = IsIpAddress()
       validation_expression.validate('127.0.0.1')    # returns ValidationResult object
    """
    def __init__(self, *args, **kw):
        super(IsIpAddress, self).__init__(IsString(),
                                          Assert(lambda x: is_ip_address(x), "Value isn't IP4 address"),
                                          chain=True,
                                          *args,
                                          **kw)


def is_number(value):
    """Function checks that value type is number.

    :param value: Value to validate.
    :return: Validation result.
    :rtype: boolean

    .. code-block:: python

       is_number('example_string')    # returns False
       is_number(10)                  # returns True
    """
    return type(value) in (int, long, float)


class IsNumber(Validator):
    """Validator is checking that value is number type.

    .. code-block:: python

       validation_expression = IsNumber()
       validation_expression.validate(10)     # returns ValidationResult object
    """
    RESULT_MESSAGE_TEMPLATE = "Is <%s> a number?: %s"

    def __init__(self, *args, **kw):
        super(IsNumber, self).__init__(*args, **kw)

    def validate(self, value, *args, **kw):
        """Method checks if specified value meet requirements."""
        result = is_number(value)
        message = self._build_message(value, result)
        return ValidationResult(value, result, message)


def is_in_range(value, from_value, to_value):
    """
    Function checks that value is between specified range.

    :param number value: Value to validate.
    :param number from_value: Beginning of range.
    :param number to_value: Ending of range.

    :return: Validation result.
    :rtype: boolean

    .. code-block:: python

       is_in_range(10, 0, 20)      # returns True
       is_in_range(10, 0, 10)      # returns False
    """
    return value >= from_value and value <= to_value


class InRange(Validator):
    """Validator is checking that value is in specified range.

    .. code-block:: python

       validation_expression = InRange(0, 20)
       validation_expression.validate(10)      # returns ValidationResult object
    """
    RESULT_MESSAGE_TEMPLATE = "Is <%s> between <%s> and <%s>?: %s"

    def __init__(self, from_value, to_value, *args, **kw):
        """
        :param number from_value: Beginning of range.
        :param number to_value: Ending of range.
        """
        super(InRange, self).__init__(*args, **kw)
        self.from_value = from_value
        self.to_value = to_value

    def validate(self, value, *args, **kw):
        """Method checks if specified value meet requirements."""
        result = is_in_range(value, self.from_value, self.to_value)
        message = self._build_message(value, self.from_value, self.to_value, result)
        return ValidationResult(value, result, message)


class ValidPortRange(And):
    """Validator is checking that value is in valid port range 0-65535.

    .. code-block:: python

       validation_expression = ValidPortRange()
       validation_expression.validate(8888)      # returns ValidationResult object
    """

    def __init__(self, *args, **kw):
        super(ValidPortRange, self).__init__(IsNumber(),
                                             Assert(lambda x: isinstance(x, int), "Value isn't integer"),
                                             InRange(0, 65535),
                                             chain=True,
                                             *args,
                                             **kw)


def is_empty(value):
    """Function checks that value is empty.

    :param value: Value to validate: dict, list, string.
    :return: Validation result.
    :rtype: boolean

    .. code-block:: python

       is_empty('')                  # returns True
       is_empty([])                  # returns True
       is_empty(0)                   # returns False
       is_empty('example_string')    # returns False
    """
    if isinstance(value, bool) or isinstance(value, int):
        return False
    return False if value else True


def is_not_empty(value):
    """Function checks that value is not empty.

    :param value: Value to validate: dict, list, string.
    :return: Validation result.
    :rtype: boolean

    .. code-block:: python

       is_not_empty('example_string')     # returns True
       is_not_empty([1])                  # returns True
       is_not_empty('')                   # returns False
       is_not_empty(1)                    # returns False
    """
    if isinstance(value, bool) or isinstance(value, int):
        return False
    return not is_empty(value)


class IsNotEmpty(Validator):
    """Validator is checking that value is not empty.

    .. code-block:: python

       validation_expression = IsNotEmpty()
       validation_expression.validate(10)       # returns ValidationResult object
    """

    RESULT_MESSAGE_TEMPLATE = "Is <%s> not empty?: %s"

    def __init__(self, *args, **kw):
        super(IsNotEmpty, self).__init__(*args, **kw)

    def validate(self, value, *args, **kw):
        """Method checks if specified value meet requirements."""
        result = is_not_empty(value)
        message = self._build_message(value, result)
        return ValidationResult(value, result, message)


def is_instance(value, classinfo):
    """Function checks that value object is an instance of the classinfo.

    :param value: Value to validate.
    :param classinfo: Class object to be compared with value argument.

    :return: Validation result.
    :rtype: boolean

    .. code-block:: python

       is_instance('example_string', str)    # returns True
       is_instance(1, str)                   # returns False

    """
    return isinstance(value, classinfo)


class IsInstance(Validator):
    """Validator is checking that value object is an instance of a class.

    .. code-block:: python

       validation_expression = IsInstance()
       validation_expression.validate(10, int)        # returns ValidationResult object
    """
    err_msg = "Is <%s> instance of <%s>?: %s"

    def __init__(self, classinfo, *args, **kw):
        """
        :param classinfo: Class instance object.
        """
        super(IsInstance, self).__init__(*args, **kw)
        self.classinfo = classinfo

    def validate(self, value, *args, **kw):
        """Method checks if specified value meet requirements."""
        result = is_instance(value, self.classinfo)
        message = IsInstance.err_msg % (value, self.classinfo, result)
        return ValidationResult(value, result, message)


class IsOneOf(Validator):
    """Validator is checking that value is one of an options.

    .. code-block:: python

       validation_expression = IsOneOf(10, 20, 'test_string, False)
       validation_expression.validate('test_string')       # returns ValidationResult object
    """
    RESULT_MESSAGE_TEMPLATE = "Is <%s> one of [%s]?: %s"

    def __init__(self, *args, **kw):
        super(IsOneOf, self).__init__(*args, **kw)
        self.options = list(args)

    def validate(self, value, *args, **kw):
        """Method checks if specified value meet requirements."""
        result = value in self.options
        message = self._build_message(value, ', '.join(str(o) for o in self.options), result)
        return ValidationResult(value, result, message)


class Matches(And):
    """Validator is checking that value match regex.

    .. code-block:: python

       validation_expression = Matches(r"\w+")
       validation_expression.validate('test_string ')     # returns ValidationResult object
    """

    def __init__(self, regex, *args, **kw):
        """
        :param str regex: Regex using in string matching.
        """
        super(Matches, self).__init__(IsString(),
                                      Assert(lambda x: bool(match(regex, x)), "Value doesn't match"),
                                      chain=True,
                                      *args,
                                      **kw)
        self.regex = regex


class ValidLength(And):
    """Validator is checking that value length is in range min_len-max_len.

    .. code-block:: python

       validation_expression = ValidLength(10, 20)
       validation_expression.validate('test_string')      # returns ValidationResult object
    """

    def __init__(self, min_len, max_len, *args, **kw):
        """
        :param integer min_len: Minimum value length.
        :param integer max_len: Maximum value length.
        """
        super(ValidLength, self).__init__(
            Assert(lambda x: hasattr(x, '__len__'), "Object doesn't support length check."),
            Assert(lambda x: is_in_range(len(x), min_len, max_len), "Value isn't in range [%d, %d]." % (min_len, max_len)),
            chain=True,
            *args,
            **kw
        )

        self.min_len = min_len
        self.max_len = max_len
