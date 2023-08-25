"""" Example showing the use of GPT Easy with data returned in a fixed format using dataclasses"""
import sys
sys.path.append('.')
import pathlib
import json
from dataclasses import dataclass

from gpteasy import GPT
from dataclasses_jsonschema import JsonSchemaMixin

""" Define your model as dataclasses with the JsonSchemaMixin """
@dataclass
class Person(JsonSchemaMixin):
    name: str
    house_number: int
    profession: str

@dataclass
class Persons(JsonSchemaMixin):
    persons: list[Person]


def get_story():
    """ Read story.txt from the path of the current file """
    path = pathlib.Path(__file__).parent / 'story.txt'
    with open(path) as f:
        return f.read()


if __name__ == "__main__":
    gpt = GPT()
    gpt.model = 'gpt-3.5-turbo'
    prompt = "Read the following story and give me a list of the persons involved. " +\
             "Each with their name, profession and house number\n\n" + get_story()
    gpt.set_return_type(Persons)

    data = gpt.chat(prompt)
    print(json.dumps(data, indent=4))
