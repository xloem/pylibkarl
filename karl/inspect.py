from inspect import *

def name(object) -> str:
    if hasattr(object, '__name__'):
        return object.__name__
    else:
        return None

def file_line_name(object) -> str:
    file = getfile(object)
    source, line = getsourcelines(object)
    name_ = name(object)
    if name_ is None:
        name_ = ''
    else:
        name_ = ' ' + name_
    return file + ':' + str(line) + name_

def annotations(function : callable) -> dict:
    sig = signature(function)
    return {
        **{
            param.name : param.annotation
            for param in signature(function).parameters
        },
        '__return' : sig.return_annotation
    }

def mutate_annotations(function : callable, mutator : callable, generator : callable = None) -> None:
    if hasattr(function, '__annotations__'):
        sig = signature(function)
        annotations = function.__annotations__
        for param in sig.parameters.values():
            if param.annotation is param.empty:
                if generator is not None:
                    annotations[param.name] = generator(param.name)
            else:
                annotations[param.name] = mutator(param.annotation)
    return function

