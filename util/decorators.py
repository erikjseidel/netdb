
def netdb_internal(func):
    """
    Checks / enforces regular returns for netdb internal methods. Wrapped 
    functions must return three vars:

    result:  (bool) whether or not result was given
    out:     (dict) dictionary containing netdb data
    comment: (str)  a brief message describing operation / result

    """
    def decorator(*args, **kwargs):
        result, out, comment = func(*args, **kwargs)

        assert isinstance(result, bool)
        assert (out == None) or isinstance(out, (list, dict)), isinstance(comment, str)

        return result, out, comment
    return decorator


def netdb_provider(func):
    """
    Enforces three tuple return and converts it to four key dict style output. 
    Wrapped functions must return three vars:

    result:  (bool) whether or not result was given
    out:     (dict) dictionary containing netdb data
    comment: (str)  a brief message describing operation / result

    This becomes: {
            'result' : bool,
            'error'  : bool,
            'out'    : dict,
            'comment': str,
            }

    If incoming 'out' is None, 'out' will not be returned in the resulting dict.

    """
    def decorator(*args, **kwargs):
        result, out, comment = func(*args, **kwargs)

        assert isinstance(result, bool)
        assert (out == None) or isinstance(out, dict), isinstance(comment, str)

        ret = { 'result': result, 'error': False, 'comment': comment }

        if out: ret.update({ 'out': out })

        return ret
    return decorator
