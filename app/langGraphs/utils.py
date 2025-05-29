def retry_on_failure(func, max_attempts=3):
    def wrapped(state):
        for attempt in range(max_attempts):
            try:
                return func(state)
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
    return wrapped
