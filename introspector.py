from __future__ import print_function

import inspect
import itertools
import reprlib

def full_sig(method):
    """Gets the inspect.signature of the supplied method
    
    Returns a predefined string if unable to get a valid signature

    Arguments:
        method (function)

    Returns
        (str)

    """
    try:
        return method.__name__ + str(inspect.signature(method))
    except ValueError:
        return method.__name__ + '(...)'


def brief_doc(obj):
    """Returns the first line of the doc string of the supplied object

    Returns an empty string if object has no doc string

    Arguments:
        obj (Object)

    Returns:
        (str)

    """
    doc = obj.__doc__
    if doc is not None:
        lines = doc.splitlines()
        if len(lines) > 0:
            return lines[0]
    return ''


def print_table(rows_of_columns, *headers):
    """Format the supplied lists in a table format

    Arguments:
        rows_of_columns (list of str)
        *headers (str)

    Returns:
        None

    """
    num_columns = len(rows_of_columns[0])
    num_headers = len(headers)
    if len(headers) != num_columns:
        raise TypeError("Expected {} header arguments, "
                        "got {}".format(num_columns, num_headers))
    rows_of_columns_with_header = itertools.chain([headers], rows_of_columns)
    columns_of_rows = list(zip(*rows_of_columns_with_header))
    column_widths = [max(map(len, column)) for column in columns_of_rows]
    column_specs = ('{{:{w}}}'.format(w=width) for width in column_widths)
    format_spec = ' '.join(column_specs)
    print(format_spec.format(*headers))
    rules = ('-' * width for width in column_widths)
    print(format_spec.format(*rules))
    for row in rows_of_columns:
        print(format_spec.format(*row))


def dump(obj):
    """Prints, in detail, information about the supplied object

    Arguments:
        obj (Object)

    Returns:
        None

    """
    print("Type")
    print("====")
    print(type(obj))
    print()

    print("Documentation")
    print("=============")
    print(inspect.getdoc(obj))
    print()

    print("Attributes")
    print("==========")
    all_attr_names = set(dir(obj))
    method_names = set(
        filter(lambda attr_name: callable(getattr(obj, attr_name)),
               all_attr_names))
    assert len(method_names) <= len(all_attr_names),\
           "len(method_names): {}, len(all_attr_names): {}".format(len(method_names), len(all_attr_names))
    attr_names = all_attr_names - method_names
    attr_names_and_values = [(name, reprlib.repr(getattr(obj, name))) for name in sorted(attr_names)]
    print_table(attr_names_and_values, "Name", "Value")
    print()

    print("Methods")
    print("=======")
    methods = (getattr(obj, method_name) for method_name in sorted(method_names))
    method_names_and_doc = [(full_sig(method), brief_doc(method)) for method in methods]
    print_table(method_names_and_doc, "Name", "Description")
    print()
