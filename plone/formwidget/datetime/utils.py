from collections import deque


def rotated(sequence, steps):
    """Returns a (shallow) copy of the ``sequence`` rotated ``steps``
    times to the right.
    """
    dq = deque(sequence)
    dq.rotate(steps)
    return list(dq)


def padded_hour(hour=None, ampm=False):
    """ Return the hour with leading zeros.

    >>> from plone.formwidget.datetime.utils import padded_hour
    >>> padded_hour(0)
    >>> '00'
    >>> padded_hour(1)
    >>> '01'
    >>> padded_hour(12)
    >>> '12'
    >>> padded_hour(24)
    >>> '24'
    >>> padded_hour(01, ampm=True)
    >>> '01'
    >>> padded_hour(12, ampm=True)
    >>> '12'
    >>> padded_hour(15, ampm=True)
    >>> '03'
    >>> padded_hour(24, ampm=True)
    >>> '12'

    """
    if hour is None: return None
    hour = int(hour)
    if ampm and hour>12:
        hour = hour-12
    return padded_value(hour)


def padded_minute(minute=None):
    """ Return the minute with leading zeros.

    >>> from plone.formwidget.datetime.utils import padded_minute
    >>> padded_minute(0)
    >>> '00'
    >>> padded_minute(5)
    >>> '05'
    >>> padded_minute(59)
    >>> '59'

    """
    if minute is None: return None
    return padded_value(minute)


def padded_value(value):
    """ Return a two character string with leading zeros.

    >>> from plone.formwidget.datetime.utils import padded_value
    >>> padded_value(0)
    >>> '00'
    >>> padded_value(5)
    >>> '05'
    >>> padded_value('a')
    >>> '0a'
    >>> padded_value('ab')
    >>> 'ab'
    >>> padded_value('abc')
    >>> 'abc'
    >>> padded_value('')
    >>> '00'

    """
    return str(value).zfill(2)
