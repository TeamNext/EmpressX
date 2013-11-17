import subprocess

from empressx.retinue import state


def _prefix_commands(command):

    prefixes = list(state.env.command_prefixes)

    cwd = state.env.cwd
    if cwd:
        prefixes.insert(0, 'cd %s' % cwd)
    glue = " && "
    return glue.join(prefixes + [command])


def local(command, capture=False, shell=None):
    wrapped_command = _prefix_commands(command)
    print wrapped_command
