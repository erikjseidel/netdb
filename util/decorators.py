
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
    Enforces four tuple return and converts it to salt style output. Wrapped 
    functions must return four vars:

    result:  (bool) whether or not result was given
    error:   (bool) whether or not there was an error
    out:     (dict) dictionary containing netdb data
    comment: (str)  a brief message describing operation / result

    This becomes: {
            'result' : bool,
            'error'  : bool,
            'out'    : dict,
            'comment': str,
            }

    """
    def decorator(*args, **kwargs):
        result, error, out, comment = func(*args, **kwargs)

        if not isinstance(result, bool):
            return { 'result': False, 'error': True,
                    'comment': 'API EXCEPTION: %s: first return (result) must be boolean.' % func.__name__ }

        if not isinstance(error, bool):
            return { 'result': False, 'error': True,
                    'comment': 'APIEXCEPTION: %s: second return (error) must be boolean.' % func.__name__ }

        if out and not isinstance(out, dict):
            return { 'result': False, 'error': True,
                    'comment': 'API EXCEPTION: %s: third return (out) must be a dict or NoneType.' % func.__name__ }

        if not isinstance(comment, str):
            return { 'result': False, 'error': True,
                    'comment': 'API EXCEPTION: %s: fourth return (comment) must be a string.' % func.__name__ }

        return { 'result': result, 'error': error, 'out': out, 'comment': comment }
    return decorator
