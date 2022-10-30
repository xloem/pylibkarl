def getname(obj : object, default='unk'):
    return obj if type(obj) is str else getattr(obj, '__name__', default)

def name(new_word : str, joiner='_'):
    '''
    Returns a decorator that updates a function's __name__ by replacing the
    last underscore-separated word with a string determined at runtime.  The new
    string may itself be an object with a __name__.  If the new string is not a
    string but is an iterable, it will be joined.
    '''
    if hasattr(new_word, '__name__'):
        new_word = new_word.__name__
    elif type(new_word) is not str:
        new_word = joiner.join((getattr(item, '__name__', item) for item in new_word))
    def update(function):
        if hasattr(function, '__name__'):
            full_old_name = function.__name__
            idx = full_old_name.rfind('_')
            function.__name__ = full_old_name[:idx+1] + new_word
        return function
    return update

def proxy_getattr_after_to_kwparam(attr_param_name : str) -> callable:
    '''
    Returns a function decorator that produces a function which, when called,
    first returns an object, then calls the decorated function whenever an
    attribute of that object is accessed, passing the attribute name via the given
    parameter.
    '''
    def decorator(function : callable) -> callable:
        class attr_class:
            def __init__(self, *params, **kwparams):
                self.params = params
                self.kwparams = kwparams
            def __getattr__(self, name):
                result = function(*self.params, **{**self.kwparams, attr_param_name: name})
                if result is None:
                    # this lets the return value be called like a function for appearances
                    result = lambda: None
                return result
        attr_class.__name__ = function.__name__
        return attr_class
    return decorator

def proxy_getattr_before_to_kwparam(attr_param_name : str) -> object:
    '''
    A function decorator that produces an object which calls the decorated
    function whenever an attribute is accessed, passing the attribute name via the
    given parameter.
    '''
    class decorator:
        def __init__(self, function : callable):
            self.__function = function
        def __getattr__(self, name):
            def wrapper(*params, **kwparams):
                return self.__function(*params, **{**kwparams, attr_param_name : name})
            wrapper.__name__ = self.__function.__name___
            return wrapper
