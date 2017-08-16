#!/usr/bin/env python
from contextlib import contextmanager
import subprocess
import sys

from iterm2_dwim.editors import emacs
from iterm2_dwim.logger import log
from iterm2_dwim.parser import get_path_and_line


Editor = emacs.Editor


def notify(message):
    subprocess.check_call([
        '/usr/local/bin/terminal-notifier',
        '-title', 'iterm2-dwim',
        '-subtitle', 'Error',
        '-message', message,
    ])


@contextmanager
def notification_on_error():
    try:
        yield
    except Exception as ex:
        msg = '%s: %s\n' % (type(ex).__name__, ex)
        notify(msg)
        log(msg)
        exit(1)


def main():
    with notification_on_error():
        path, line = get_path_and_line(*sys.argv[1:])

    with notification_on_error():
        Editor().edit_file(path, line)
