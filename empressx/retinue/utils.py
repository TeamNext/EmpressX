import subprocess

from empressx.retinue.conf import settings
from empressx.retinue.exceptions import CommandExecutionError


def localcommand(command):
    p = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    return_code = p.returncode

    if return_code:
        raise CommandExecutionError("(return code %d) the outputs is:\n%s"
                                    % (return_code, stdout))
    else:
        return stdout


def virtualenvcommand(command):
    commands = [
        'source %s' % settings.RETINUE_VIRTUALENVWRAPPER_PATH,
        command
    ]

    return localcommand(' && '.join(commands))
