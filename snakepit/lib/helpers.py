"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""

import time
from os.path import join as join_path
from routes import url_for
from webhelpers.html import tags, tools, escape as _escape, literal as _literal
from snakepit.lib import to_unicode

def escape(text):
    return _escape(to_unicode(text))

def literal(text):
    return _literal(to_unicode(text))

def timestamp():
    return int(time.time())

def required():
    return _literal('<span class="required">*</span>')

TIME_WORDS = ['second', 'minute', 'hour', 'day', 'week', 'year', 'decade']

def time_ago_in_words(seconds, units=2):
    
    def output(*args):
        params = []
        for index, arg in enumerate(args):
            arg = int(arg)
            if arg == 0:
                continue
            text = (arg >= 2 and TIME_WORDS[index] + 's') or TIME_WORDS[index]
            params.append('%d %s' % (arg, text))
        params.reverse()
        return ', '.join(params[0:units])
    
    if seconds == 0:
        return 'less than a second'
    
    if seconds < 60:
        return seconds > 1 and '%d seconds' % seconds or '1 second'
    
    minutes = seconds / 60
    seconds = seconds % 60
    if minutes < 60:
        return output(seconds, minutes)
    
    hours = minutes / 60
    minutes = minutes % 60
    if hours < 24:
        return output(seconds, minutes, hours)
    
    days = hours / 24
    hours = hours % 24
    if days < 7:
        return output(seconds, minutes, hours, days)
    
    weeks = days / 7
    days = days % 7
    if weeks < 52:
        return output(seconds, minutes, hours, days, weeks)
    
    years = weeks / 52
    weeks = years % 52
    if years < 10:
        return output(seconds, minutes, hours, days, weeks, years)
    
    decades = years / 10
    years = years % 10
    return output(seconds, minutes, hours, days, weeks, years, decades)

def time_ago(timestamp, units=2):
    if timestamp is None:
        return ''
    now = time.time()
    seconds = now - int(timestamp)
    return time_ago_in_words(seconds, units)

def pretty_bytes(bytes):
    if bytes < 1024:
        return "%s bytes" % bytes
    bytes = bytes / 1024.0
    if bytes < 1024:
        return "%s kB" % round(bytes, ndigits = 1)
    bytes = bytes / 1024.0
    if bytes < 1024:
        return "%s mB" % round(bytes, ndigits = 1)
    return bytes;