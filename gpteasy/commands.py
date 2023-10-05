""" Handles special commands starting with : to set system parameters or model parameters """
from .display import color_print, ERROR_COLOR, SYSTEM_COLOR, ASSISTANT_COLOR
from .gpt import GPT


class CommandHandler:
    def __init__(self, gpt: GPT):
        self.gpt = gpt

        self.commands = {}
        self.add_command('quit', self.handle_quit, ":quit - Quit the program")
        self.add_command('load', self.handle_load, ":load name - loads the saved conversation with the specified name")
        self.add_command('save', self.handle_save, ":save name - saves the conversation under the specified name")
        self.add_command('debug', self.handle_debug, ":debug - set to True displays all prompts and model replies")
        self.add_command('input', self.handle_input, ":input filename - loads an input from the specified file")
        self.add_command('model', self.handle_gpt_attribute, ":model gpt-4 - Sets the AI model")
        self.add_command('system', self.handle_system, ":system system_message - Sets the system message for the model.")
        self.add_command('max_tokens', self.handle_gpt_attribute,
                         ":max_tokens 800 - The maximum number of tokens to generate in the completion")
        self.add_command('temperature', self.handle_gpt_attribute, ":temperature 0.9 - What sampling temperature to " +
                                                                   "use, between 0 and 2")
        self.add_command('n', self.handle_gpt_attribute, ":n 1 - Specifies the number answers given")
        self.add_command('stop', self.handle_gpt_attribute, ':stop ["\\n", " Human:", " AI:"] - Up to 4 sequences ' +
                                                            'where the API will stop generating further tokens')
        self.add_command('bye', self.handle_bye, ":bye - quits but saves the conversation first")
        self.add_command('help', self.handle_help, ":help - shows this help message")
        for attr in dir(self.gpt):
            if attr[0] != '_' and attr not in self.commands:
                self.add_command(attr, self.handle_gpt_attribute, "")

    def add_command(self, command, handler, description):
        self.commands[command] = (handler, description)

    def handle_quit(self):
        return False

    def handle_load(self, filename):
        if filename:
            self.gpt.load(filename)
        else:
            color_print(f"Pass a filename\n", color=ERROR_COLOR)
        return True

    def handle_input(self, filename):
        if filename:
            self.gpt.file_input(filename)
        else:
            color_print(f"Pass a filename\n", color=ERROR_COLOR)
        return True

    def handle_save(self, filename=None):
        if not filename:
            filename = self.gpt.name
        self.gpt.save(filename)
        color_print(f"Saved to {(self.gpt.save_dir / filename).with_suffix('.txt')}\n", color=SYSTEM_COLOR)
        return True

    def handle_system(self, system_message):
        if not system_message:
            color_print(f"Pass a system message\n", color=ERROR_COLOR)
            return True
        self.gpt.system_message = system_message
        color_print(f"System message set to ", color=SYSTEM_COLOR)
        color_print(f"{system_message}\n", color=ASSISTANT_COLOR)
        return True

    def handle_reset(self):
        self.gpt.reset()
        color_print(f"Conversation reset\n", color=SYSTEM_COLOR)
        return True

    def handle_debug(self, debug: str = None):
        if debug is None:
            color_print(f'debug is {self.gpt.debug}', color=SYSTEM_COLOR)
        else:
            self.gpt.debug = debug.lower() in ['true', '1', 't', 'y', 'yes']
            color_print(f'debug set to {self.gpt.debug}', color=SYSTEM_COLOR)
        return True

    def handle_bye(self):
        self.gpt.save()
        self.gpt.chat('bye')
        return False

    def handle_maxmessages(self, param):
        self.gpt.message_memory = int(param)

    def handle_gpt_attribute(self, attr, value):
        if not value:
            value = getattr(self.gpt, attr)
            color_print(f"{attr} is currently {value}\n", color=SYSTEM_COLOR)
            return True
        try:
            value = eval(value)
        except (SyntaxError, NameError):
            pass  # Treat param as a string
        setattr(self.gpt, attr, value)
        color_print(f"{attr} set to {value}\n", color=SYSTEM_COLOR)
        return True

    def handle_help(self):
        for (_, description) in self.commands.values():
            if description:
                color_print(description, color=SYSTEM_COLOR)
        return True

    def handle_command(self, command: str):
        # Commands can be things like
        # :load filename
        # :save [filename]
        # :quit
        # :max_tokens=1000
        # :temperature=0.8
        if command.count('='):
            command, param = command.split('=', 1)
        elif command.count(' '):
            command, param = command.split(' ', 1)
        else:
            param = None
        if command not in self.commands:
            color_print(f"Unknown command: {command}\n", color=ERROR_COLOR)
            return True
        handler, _ = self.commands[command]
        if handler == self.handle_gpt_attribute:
            return handler(command, param)
        if param:
            return handler(param)
        return handler()
