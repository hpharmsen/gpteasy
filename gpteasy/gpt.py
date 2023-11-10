""" Handles the GPT API and the conversation state. """
import json
import os
import re
import sys
from pathlib import Path

import openai
from openai import APIConnectionError, APIError, RateLimitError, OpenAI
from dotenv import load_dotenv

from gpteasy.display import print_message, color_print, SYSTEM_COLOR, ERROR_COLOR, DEBUG_COLOR2, DEBUG_COLOR1

BASE_SYSTEM = "You are ChatGPT, a large language model trained by OpenAI."
DEFAULT_PARAMETERS = {"type": "object", "properties": {}, "required": []}

class GptFunction:
    def __init__(self, name: str, description: str, parameters=None, callback=None):
        self.function_name = name
        self.description = description
        self.parameters = parameters if parameters else DEFAULT_PARAMETERS  # name: (type, description, required, enum)
        self.callback = callback

    def add_param(self, name: str, type: str, description: str = None, required: bool = False, enum: list = None):
        self.parameters[name] = (type, description, required, enum)

    def __call__(self, **kwargs):
        return self.callback(**kwargs)

    def in_completion_format(self) -> dict:
        """{
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        },
                    },
                    "required": ["location"],
                },
            }"""
        function = {
            "name": self.function_name,
            "description": self.description,
            "parameters": self.parameters
        }
        if not self.parameters:
            for name, (type, description, required, enum) in self.parameters.items():
                param_values = {"type": type}
                if description:
                    param_values["description"] = description
                if enum is not None:
                    param_values["enum"] = enum
                function["parameters"]["properties"][name] = param_values
                if required:
                    function["parameters"]["required"].append(name)
        return function


class GPT:
    def __init__(self):
        # Authentication
        if not os.getenv("OPENAI_API_KEY"):
            load_dotenv()  # Load the .env file into the environment
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            color_print("No OpenAI API key found. Create one at https://platform.openai.com/account/api-keys and " +
                        "set it in the .env file like OPENAI_API_KEY=here_comes_your_key.", color=ERROR_COLOR)
        self.client = OpenAI()
        self.functions = {}  # Callable GPT functions
        self.return_type = None  # Structure of the data of the function called by the model. Default is text.

        self.system_message = BASE_SYSTEM

        # Model parameters
        self.model = "gpt-3.5-turbo"  # or "gpt-4"

        # The maximum number of tokens to generate in the completion.
        # Defaults to 16
        # The token count of your prompt plus max_tokens cannot exceed the model's context length.
        # Most models have a context length of 2048 tokens (except for the newest models, which support 4096).
        self.max_tokens = 800

        # What sampling temperature to use, between 0 and 2.
        # Higher values like 0.8 will make the output more random, while lower values like 0.2
        # will make it more focused and deterministic.
        # We generally recommend altering this or top_p but not both
        # Defaults to 1
        self.temperature = 0.9

        # An alternative to sampling with temperature, called nucleus sampling,
        # where the model considers the results of the tokens with top_p probability mass.
        # So 0.1 means only the tokens comprising the top 10% probability mass are considered.
        # We generally recommend altering this or temperature but not both.
        # Defaults to 1
        self.top_p = 1

        # How many completions to generate for each prompt.
        # Because this parameter generates many completions, it can quickly consume your token quota.
        # Use carefully and ensure that you have reasonable settings for max_tokens and stop.
        self.n = 1

        # Up to 4 sequences where the API will stop generating further tokens.
        # The returned text will not contain the stop sequence.
        # Example: [" Human:", " AI:"]
        self.stop = None

        # Number between -2.0 and 2.0.
        # Positive values penalize new tokens based on whether they appear in the text so far,
        # increasing the model's likelihood to talk about new topics.
        # Defaults to 0
        self.presence_penalty = 0

        # Number between -2.0 and 2.0.
        # Positive values penalize new tokens based on their existing frequency in the text so far,
        # decreasing the model's likelihood to repeat the same line verbatim.
        # Defaults to 0
        self.frequency_penalty = 0

        # Parameters to save the current conversation
        self.name = ''  # Name of the current conversation
        self.save_dir = Path(__file__).resolve().parent / 'saves'
        self.save_dir.mkdir(exist_ok=True)
        self.message_memory = 20  # Number of messages to remember. Limits token usage.
        self.messages = []

        self.debug = False

    @classmethod
    def from_json(cls, s):
        gpt = cls()
        dictionary = json.loads(s)
        for key, value in dictionary.items():
            match key:
                case 'save_dir':
                    gpt.save_dir = Path(value)
                case 'messages':
                    gpt.messages = [Message.from_dict(m) for m in value]
                case _:
                    setattr(gpt, key, value)
        return gpt

    def set_api_key(self, key: str):
        """ Used when using GPTEasy from a browser where the user has to specify a key """
        openai.api_key = key

    def system(self):  # This function can be overwritten by child classes to make the system message dynamic
        return self.system_message

    def reset(self):
        self.name = ''
        self.messages = []

    def get_messages(self):
        result = [{'role': 'system', 'content': self.system()}]
        for m in self.messages[-self.message_memory:]:
            message = {'role': m.role, 'content': m.text}
            if m.function_name:  # Function name in case the model called a function
                message['name'] = m.function_name
            if m.function_content:  # Function result in case the model called a function
                message['content'] = m.function_content
            result.append(message)
        return result

    def last_token_count(self):
        return self.messages[-1].tokens() if self.messages else 0

    def add_function(self, function: GptFunction):
        self.functions[function.function_name] = function

    def set_return_type(self, model):
        self.return_type = [{
                    "name": model.__name__,
                    "description": model.__doc__,
                    "parameters": model.json_schema()}]

    def remove_funtion(self, name: str):
        del self.functions[name]

    def get_functions(self):
        """ Specifying a return type misuses the function calling mechnism. In this case return the return type.
        """
        if self.return_type:
            return self.return_type

        return [f.in_completion_format() for f in self.functions.values()] if self.functions else None

    def chat(self, prompt, add_to_messages=True):

        def chat_completion_request(function_call="auto"):
            if self.debug:
                color_print(f"\nRunning completion with these messages", color=DEBUG_COLOR1)
                for message in self.messages:
                    if hasattr(message, 'text'):
                        color_print(f"{message}", color=DEBUG_COLOR1)
                if self.functions:
                    color_print(f"And these functions", color=DEBUG_COLOR1)
                    for function in self.functions.values():
                        color_print(f"{function.function_name}({function.parameters})", color=DEBUG_COLOR1)
                print()

            messages = self.get_messages()
            functions = self.get_functions()
            for _ in range(3):
                try:
                    if functions:
                        completion = self.client.chat.completions.create(
                            model=self.model,
                            messages=messages,
                            temperature=self.temperature,
                            max_tokens=self.max_tokens,
                            n=self.n,
                            top_p=self.top_p,
                            frequency_penalty=self.frequency_penalty,
                            presence_penalty=self.presence_penalty,
                            stop=self.stop,
                            functions=functions,
                            function_call=function_call
                        )
                    else:  # Version for models without the possibility to use functions
                        completion = self.client.chat.completions.create(
                            model=self.model,
                            messages=messages,
                            temperature=self.temperature,
                            max_tokens=self.max_tokens,
                            n=self.n,
                            top_p=self.top_p,
                            frequency_penalty=self.frequency_penalty,
                            presence_penalty=self.presence_penalty,
                            stop=self.stop
                        )
                    if self.debug and hasattr(completion.choices[0], 'text'):
                        color_print(f"{completion.choices[0].text}", color=DEBUG_COLOR2)
                    return completion
                except APIConnectionError as e:
                    color_print("Connection error.", color=SYSTEM_COLOR)
                except APIError as e:
                    color_print("API error", color=SYSTEM_COLOR)
                except RateLimitError as e:
                    color_print(f"{self.model} is overloaded", color=SYSTEM_COLOR)
            sys.exit('Too many errors. Aborting.')

        if self.messages and not self.name:
            self.name = re.sub(r'\W+', '', self.messages[0].text).replace(' ', '_')[:20]
        self.messages += [Message('user', prompt)]

        completion = chat_completion_request()

        while not self.return_type and completion.choices[0].finish_reason == 'function_call':
            message = completion.choices[0].message
            completion.choices[0].message.function_call
            function_call = message.function_call
            function_to_call = self.functions[function_call.name]
            kwargs = json.loads(function_call.arguments)
            function_response = function_to_call(**kwargs)

            self.messages += [Message('function', function_name=function_call.name, function_content=function_response)]

            # get a new response from GPT where it can see the function response
            completion = chat_completion_request(function_call="none")

            # Special case: sometimes the model returns a sql query instead of the answer
            # In this case explain this to the model and ask for the answer.

        message_text = completion.choices[0].message.content
        message = Message('assistant', message_text)
        if add_to_messages:
            self.messages += [message]

        if self.return_type and completion.choices[0].message.function_call:
            # This indicates a return type is used. Return the data in a structured format
            message.text = completion.choices[0].message.function_call.arguments
            return json.loads(message.text)

        return message.text

    def after_response(self):
        # content is in messages[-1]['completion']['choices'][0]['message']['content']
        return  # Can be overridden

    def save(self, name=None):
        if name:
            self.name = name

        with open((self.save_dir / self.name).with_suffix('.txt'), "w") as f:
            f.write(f"system: {self.system()}\n")
            for message in self.messages:
                f.write(f"{message.role}: {message.text}\n")

    def load(self, name):
        def save_message(msg):
            if msg.role == 'system':
                self.system_message = msg.text
            else:
                self.messages += [msg]

        self.messages = []
        self.name = name
        if not name.endswith('.txt'):
            name += '.txt'
        filename = self.save_dir / name
        if not os.path.isfile(filename):
            color_print(f"New conversation:  {filename}", color=SYSTEM_COLOR)
            return
        with open(filename, "r") as f:
            message = Message()
            assert not message
            for line in f.readlines():
                line = line[:-1]
                try:
                    role, text = line.split(': ', 1)
                except ValueError:
                    message.text += '\n' + line
                    continue
                if role in ['system', 'user', 'assistant', 'function']:
                    if message:
                        save_message(message)
                    message = Message(role=role, text_or_completion=text)
                else:
                    message.text += '\n' + line
            if message:
                save_message(message)
        print_message(Message('system', self.system()), 'system')
        for message in self.messages:
            print_message(message.text, message.role)

    def file_input(self, filename):
        with open(filename, "r") as f:
            prompt = f.read()
        self.chat(prompt)

    def dumps(self) -> str:
        dict = {}
        for key, value in self.__dict__.items():
            if value is not None:
                try:
                    json.dumps(value)
                    dict[key] = value
                except  (TypeError, ValueError):
                    match key:
                        case 'save_dir':
                            dict[key] = str(value)
                        case 'messages':
                            dict[key] = [message.to_dict() for message in value]
        return json.dumps(dict, indent=2)


class Message:
    """ Handles the completion as returned by GPT """
    def __init__(self, role=None, text_or_completion=None, function_name=None, function_content=None):
        self.role = role
        if isinstance(text_or_completion, str):
            self.text = text_or_completion
            self.raw_completion = None
        else:
            self.raw_completion = text_or_completion
            self.text = text_or_completion.choices[0].message.content if text_or_completion else ''
        self.function_name = function_name  # Name of the function called in case model called a function
        self.function_content = function_content  # Result of the function called in case model called a function

    @classmethod
    def from_dict(cls, dict):
        message = cls()
        for key, value in dict.items():
            setattr(message, key, value)
        return message

    def content(self):
        try:
            return json.loads(self.raw_completion['choices'][0]['message']['content'])
        except json.decoder.JSONDecodeError:
            return {'type': 'other', 'response': self.raw_completion['choices'][0]['message']['content']}

    def tokens(self):
        return self.raw_completion.usage.total_tokens

    def __bool__(self):
        return bool(self.raw_completion) or bool(self.text)

    def __str__(self):
        res = f'role: {self.role}'
        if self.text:
            res += f' text: {self.text}'
        if self.raw_completion:
            res += f' raw_completion: {self.raw_completion}'
        if self.function_name:
            res += f' function_name: {self.function_name}'
        if self.function_content:
            res += f' function_content: {self.function_content}'
        return res

    def to_dict(self):
        dictionary = {}
        for key, value in self.__dict__.items():
            if value is not None:
                dictionary[key] = value
        return dictionary
