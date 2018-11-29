#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the minifold project.
# https://github.com/nokia/minifold

__author__     = "Marc-Olivier Buob"
__maintainer__ = "Marc-Olivier Buob"
__email__      = "marc-olivier.buob@nokia-bell-labs.com"
__copyright__  = "Copyright (C) 2018, Nokia"
__license__    = "BSD-3"

import re
from html       import escape

PATTERN_URL = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

#def str_to_html(s :str) -> str:
#    if PATTERN_URL.match(s):
#        return "<a href=%s>%s</a>" % (s, s)
#    else:
#        return s.rstrip(".").rstrip(",")

def str_to_html(s :str) -> str:
    #return escape(s).rstrip(".").rstrip(",")
    return s.rstrip(".").rstrip(",")

def dict_to_html(d :dict, keys :list, map_label :dict = dict()) -> str:
    html = "\n<table>\n"
    for k in keys:
        try:
            value = d[k]
            if value != None:
                label = map_label.get(k, k).title()
                html += "  <tr><th>%s</th><td>%s</td></tr>\n" % (
                    label,
                    value_to_html(value)
                )
        except KeyError:
            pass
    html += "</table>\n"
    return html

def to_html_link(d :dict, k :str, v :str) -> str:
    try:
        return "<a href=\"%s\">%s</a>" % (d[k], escape(v))
    except KeyError:
        return v

def value_to_html(x) -> str:
    if isinstance(x, dict):
        ret = dict_to_html(x, x.keys())
    elif isinstance(x, str):
        if PATTERN_URL.match(x):
            ret = "<a href=\"%s\">%s</a>" % (x, escape(x))
        else:
            ret = str_to_html(x)
    elif isinstance(x, (list, set)):
        ret = ", ".join([value_to_html(value) for value in x])
    else:
        ret = escape("%s" % x)
    return ret


def entries_to_html(entries :list) -> str:
    if not entries: return ""
    return "<table>\n  %(headers)s  %(data)s\n</table>" % {
        "headers" : "<tr>\n    %(row)s\n  </tr>" % {
            "row" : "\n    ".join([
                "<th>%s</th>" % k for k in sorted(entries[0].keys())
            ])
        },
        "data" : "\n".join([
            "  <tr>\n    %s\n  </tr>" % (
                "\n    ".join([
                    "<td>%s</td>" % entry[k] for k in sorted(entry.keys())
                ])
            ) for entry in entries
        ])
    }

def html(s :str):
    """
    Evaluate HTML code in a Jupyter Notebook.
    Args:
        s: A str containing HTML code.
    """
    from IPython.display import display, HTML
    chart = HTML(s)
    # or chart = charts.plot(...)
    display(chart)

def print_error(x):
    """
    Print an error in a Jupyter Notebook.
    """
    print(str(x), file = sys.stderr)

