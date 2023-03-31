
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

        if not isinstance(result, bool):
            return False, None, 'API EXCEPTION: %s: first return (result) must be boolean.' % func.__name__

        if out and not isinstance(out, dict) and not isinstance(out, list):
            return False, None, 'API EXCEPTION: %s: second return (out) must be a dict, list or NoneType.' % func.__name__

        if not isinstance(comment, str):
            return False, None, 'API EXCEPTION: %s: third return (comment) must be a string.' % func.__name__

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

        except Exception as e:
            ret = { 'result': False, 'error': True }

            if hasattr(e, 'message'):
                ret.update({ 'comment': e.message })
            else:
                exc_info = sys.exc_info()
                ret.update({ 'comment': ''.join(traceback.format_exception(*exc_info)) })

            return ret

        if not isinstance(result, bool):
            return { 'result': False, 'error': True,
                    'comment': 'API EXCEPTION: %s: first return (result) must be boolean.' % func.__name__ }

        if out and not isinstance(out, dict):
            return { 'result': False, 'error': True,
                    'comment': 'API EXCEPTION: %s: third return (out) must be a dict or NoneType.' % func.__name__ }

        if not isinstance(comment, str):
            return { 'result': False, 'error': True,
                    'comment': 'API EXCEPTION: %s: fourth return (comment) must be a string.' % func.__name__ }

        ret = { 'result': result, 'error': False, 'comment': comment }

        if out: ret.update({ 'out': out })

        return ret
    return decorator