'''
Simple boolean predicate generators.
'''
import builtins
from . import sugar

def any(*preds : list) -> callable:
    @sugar.name(preds, '_or_')
    def preds(value) -> bool:
        return builtins.any((pred(value) for pred in preds))
    return any

def all(*preds : list) -> callable:
    @sugar.name(preds, '_and_')
    def preds(value) -> bool:
        return builtins.all((pred(value) for pred in preds))
    return all
