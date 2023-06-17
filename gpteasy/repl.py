""" Class to handle the interactivity to the model and setting model system parameters """
from .display import print_message
from .gpt import GPT


class Repl:
    def __init__(self, gpt: GPT, command_handler: callable):
        self.gpt = gpt
        self.command_handler = command_handler
        self.show_token_count = False

    def run(self, first_prompt=''):
        while True:
            if first_prompt:  # If we have a first prompt, use it instead of asking the user first
                prompt = first_prompt
                first_prompt = None
            else:
                prompt = self.get_prompt()
            if prompt[0] == ':' or prompt[0] == '/':
                if not self.command_handler(prompt[1:]):
                    break
            else:
                message = self.gpt.chat(prompt)
                print_message(message)
                self.gpt.after_response(message)
                if self.show_token_count:
                    print(f"[{message.tokens()}]")

    def get_prompt(self):
        """ Default implementation, can be overridden """
        prompt = ''
        while not prompt:
            prompt = input("You: ")
        return prompt
