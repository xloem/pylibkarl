import sugar

def constructed_with(*params, **kwparams)
    ## in order to compare multiply-instantiated inner functions for equality without making them all unique,
    ## a simple solution would be to attach their local frame or parameters of construction, to their bodies
    def constructed_with_params(function : callable) -> callable:
        function.__name__ += '_' + sugar.nameof(params + tuple(kwparams.values()), '_')
