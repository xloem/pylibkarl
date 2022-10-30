from . import sugar

def visitedattr(name):
    return '__visited_' + name + '__'

def visited(object, name):
    return getattr(object, visitedattr(name), False) is True
        
def mark_visited(object, name):
    setattr(object, visitedattr(name), True)
    return object
