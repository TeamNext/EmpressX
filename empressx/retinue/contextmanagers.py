from contextlib import contextmanager

from empressx.retinue import state


@contextmanager
def _setenv(variables):
    """
    Context manager temporarily overriding ``env`` with given key/value pairs.

    A callable that returns a dict can also be passed. This is necessary when
    new values are being calculated from current values, in order to ensure that
    the "current" value is current at the time that the context is entered, not
    when the context manager is initialized. (See Issue #736.)

    This context manager is used internally by `settings` and is not intended
    to be used directly.
    """
    if callable(variables):
        variables = variables()
    clean_revert = variables.pop('clean_revert', False)
    previous = {}
    new = []
    for key, value in variables.iteritems():
        if key in state.env:
            previous[key] = state.env[key]
        else:
            new.append(key)
        state.env[key] = value
    try:
        yield
    finally:
        if clean_revert:
            for key, value in variables.iteritems():
                # If the current env value for this key still matches the
                # value we set it to beforehand, we are OK to revert it to the
                # pre-block value.
                if key in state.env and value == state.env[key]:
                    if key in previous:
                        state.env[key] = previous[key]
                    else:
                        del state.env[key]
        else:
            state.env.update(previous)
            for key in new:
                del state.env[key]


def cd(path):
    path = path.replace(' ', '\ ')
    if state.env.get('cwd') and not path.startswith('/'):
        new_cwd = state.env.get('cwd') + '/' + path
    else:
        new_cwd = path
    return _setenv({'cwd': new_cwd})


def prefix(command):
    return _setenv(lambda: {'command_prefixes': state.env.command_prefixes + [command]})