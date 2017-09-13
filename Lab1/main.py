"""
Entry point for Lab1 with CLI.
"""
import signal
import sys

from commands import Commands
from Data.datarepository import DataRepository

data = DataRepository()
commands = Commands(data)

def __sigint_handler(signum, frame):
    # commands.run('save')
    sys.exit(0)

def __main():
    # Windows 10 does not close python proccess after Ctrl-C for some reason
    signal.signal(signal.SIGINT, __sigint_handler)
    # commands.run('load')
    commands.run('help')

    try:
        __input_loop(commands)
    except (KeyboardInterrupt,  EOFError):
        __sigint_handler(None, None)


def __input_loop(commands: Commands):
    input_command = ""
    while input_command != 'exit':
        print(">", end=' ')
        input_command = input()
        words = input_command.split(' ')
        arg = None
        if words.__len__() == 3:
            arg = words[2]
            words.pop(2)

        command = '_'.join(words)
        commands.run(command, arg)

if __name__ == '__main__':
    __main()
