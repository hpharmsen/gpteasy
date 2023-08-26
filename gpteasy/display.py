""" Just some color coded output to the terminal """
import rich

ASSISTANT_COLOR = '#99ccff'
SYSTEM_COLOR = '#ffa500'
USER_COLOR = '#ffffff'
ERROR_COLOR = '#ff0000'

DEBUG_COLOR1 = '#cccccc'
DEBUG_COLOR2 = '#666666'


def color_print(text, color, end='\n'):
    rich.get_console().print(text, style=color, end=end)


def print_message(message, role):
    colors = {'assistant': ASSISTANT_COLOR, 'system': SYSTEM_COLOR, 'user': USER_COLOR}
    color = colors[role]

    end = '\n' if color == USER_COLOR else '\n\n'
    color_print(message, color=color, end=end)
