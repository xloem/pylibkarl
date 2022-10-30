'''
I define type decorators to be boolean predicates that return True if a
parameter is of the correct type.

As a shorthand, I define that bare types may be treated as being passed to the
isa() predicate generator.
'''

import builtins
from . import inspect, sugar, pred
from .pred import any, all
import warnings

def isany(value : object) -> bool:
    return True

def istype(value : isany):
    return callable(value) or value is None or type(value) is type

def matchestype(type : istype) -> istype:
    # could hand off to stdtype
    if type is None:
        return isnone
    elif builtins.type(type) is builtins.type:
        return isa(type)
    else:
        return type

#class typesugar:
#    def __init__(self, type : istype)
#        '''A type decorator that adds convenient functionality such as __and__ and __or__.'''
#        self.__type = type
#        self.__name__ = type.__name__
#    def __call__(self, *params, **kwparams):
#        return self.__type(*params, **kwparams)
#    def __and__(self, *params):
#        return 

#def stdtype(decorator : any(istype, callable)) -> callable:
#    '''
#    Standardise a type decorator or annotated function, such that decorators
#    are boolean unary predicates.
#    '''
#    if type(decorator) is type:
#        return isa(decorator)
#    elif decorator is None:
#        return isnone
#    else:
#        if not recurs.visited(decorator, 'stdtype'): # some consider implementation too slow for parse time
#            recurs.mark_visited(decorator, 'stdtype')
#            return inspect.mutate_annotations(decorator, stdtype)

def isa(type : builtins.type) -> callable:
    @sugar.named(type)
    def is_type(value : object) -> bool:
        return builtins.isinstance(value, type)
    return is_type

def isnone(value : object) -> bool:
    return value is None

def isiterable(value : object) -> bool:
    try:
        for item in value:
            return True
    except TypeError:
        return False

def lenof(len : int) -> istype:
    @sugar.named(len)
    def len_is_len(value : isany):
        try:
            return builtins.len(value) == len
        except:
            return False
    return len_is_len

def iterable_of_all(type : istype) -> bool:
    # this seems good to break out the parts of
    @sugar.named(type)
    def iterable_of_type(values : isiterable) -> bool:
        try:
            istype = matchestype(type)
            return all((istype(value) for value in values))
        except TypeError:
            return False
    return iterable_of_type

def iterable_of(*types : iterable_of_all(istype)) -> bool:
    types = [matchestype(type) for type in types]
    total_count = len(types)
    @sugar.named(types)
    def iterable_of_types(values : isiterable) -> bool:
        count = 0
        for value, type in zip(values, types):
            count += 1
            if not type(value):
                return False
        return count == total_count
    return iterable_of_types

def dict_of_all(type : istype) -> bool:
    iterable_of_2tuple = iterable_of(all(isa(tuple), lenof(2)))
    @sugar.named(type)
    def dict_of_type(dict : builtins.dict) -> bool:
        try:
            items = list(dict.items())
        except:
            return False
        if not iterable_of_2tuple(items):
            return False
        return all((istype(value) and dict[name] == value for name, value in items))
    return dict_of_type

'''useful types'''
iscallable = callable
isbool = isa(bool)
isint = isa(int)
isfloat = isa(float)

def passableto(callable : builtins.callable) -> callable:
    '''
    Returns a function that evalutes if its arguments match callable_'s annotations.
    '''
    annotations = inspect.annotations(callable)
    fln = inspect.file_line_name(callable)
    #ret = matchestype(annotations['__return']) # matching the return type atm likely would mean not multiply-instantiating function specializations

    for name, value in annotations.items():
        if value is inspect.annotations.empty:
            warnings.warn(f'The {name} parameter to {fln} is missing its annotation.')

    def passable_to_callable(*params, __return : istype = None, **kwparams) -> bool:
        '''
        Evalutes whether its arguments match the callable's annotations.
        '''
        # matching the return type atm likely would mean not multiply-instantiating function specializations
        #if (
        #    __return is not None and
        #    matchestype(__return) != ret
        #):
        #    return False
        try:
            binding = inspect.bind(callable, *params, **kwparams)
        except:
            return False
        return builtins.all((
            matchestype(annotations[name])(value)
            for name, value
            in binding.items()
        ))
    passable_to_callable.__name__ = 'passable_to_' + callable.__name__
    passable_to_callable.annotations = annotations
    passable_to_callable.file_line_name = fln

    return passable_to_callable

def callableas(*params, __return : istype = None, **kwparams) -> istype:
    @sugar.named(params if __return is None else [*params, __return])
    def callable_as_params(callable : iscallable) -> bool:
        return passableto(callable)(*params, **kwparams, __return=__return)
    return callable_as_params

pred.ispred = callableas(isany, __return = isbool)

if __name__ == '__main__':
    assert pred.ispred(pred.ispred)
    print(pred.ispred.__name__, ' => ', pred.ispred(pred.ispred))
