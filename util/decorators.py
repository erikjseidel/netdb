
import traceback
import sys

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


def salty(func):
    """
    Enforces three tuple return and converts it to salt style output. Wrapped 
    functions must return three vars:

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

    If an excecption is caught, the 'error' key will be set to 'True' and
    either the exception message (in the case of exceptions that have messages)
    or a traceback will be loaded into the 'comment' key.

    """
    def decorator(*args, **kwargs):
        try:
            result, out, comment = func(*args, **kwargs)

            assert isinstance(result, bool)
            assert (out == None) or isinstance(out, dict), isinstance(comment, str)

        except Exception as e:
            ret = { 'result': False, 'error': True }

            if hasattr(e, 'message'):
                ret.update({ 'comment': e.message })
            else:
                exc_info = sys.exc_info()
                ret.update({ 'comment': ''.join(traceback.format_exception(*exc_info)) })

            return ret

        ret = { 'result': result, 'error': False, 'comment': comment }

        if out: ret.update({ 'out': out })

        return ret
    return decorator
