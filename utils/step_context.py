def step(name):
    def decorator(func):
        func._step_name = name
        return func
    return decorator