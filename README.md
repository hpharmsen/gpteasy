# GPT Easy

Package to make working with the OpenAI GPT API in Python super easy.

Author: Hans-Peter Harmsen (hp@harmsen.nl) \
Current version: 1.3.2

## Installation
1. Install the package:
~~~~bash
python -m pip install gpteasy
~~~~
2. Create an OpenAI acccount [here](https://platform.openai.com/)
3. Create OpenAI api keys [here](https://platform.openai.com/account/api-keys)
4. Create a .env file with the following content:
```bash
OPENAI_API_KEY=your-openai-api-key
OPENAI_ORGANIZATION=your-openai-organization-id
```
## Usage
```Python
from gpteasy import GPT


if __name__ == "__main__":
    gpt = GPT()
    gpt.model = 'gpt-3.5-turbo' # Optional, the default model is gpt-4
    gpt.system = lambda: "You are a movie critic. I feed you with movie titles and you give me a review in 50 words."

    message = gpt.chat("Forrest Gump")
    print(message.text)
```
output
```
Forrest Gump is an American classic that tells the story of
a man with a kind heart and simple mind who experiences major
events in history. Tom Hanks gives an unforgettable performance, 
making us both laugh and cry. A heartwarming and nostalgic 
movie that still resonates with audiences today.
```

## Using the examples
Install dependencies:
```bash
python -m pip install -r requirements.txt
```


### Basic
```bash
python examples/basic.py
```
Starts an interactive session. In the session you dan chat with GPT-4 or another model.

### Function calling
```bash
python examples/function_calling.py
```
Example of the function calling feature. This feature allows you to call functions from within the GPT-4 model.
In this case, we query a wheather API to get the current weather.

### Specifying a return type
```bash
python examples/return_types.py
```
You can specify a specific return type (like a list of dicts) for the completion. 
This is useful when you want to extract structured data from the completion.

To define a return type, specify it as a @dataclass derived from 
[dataclasses-jsonschema](https://pypi.org/project/dataclasses-jsonschema/). 

See the example code for more details.

### Interactive
```bash
python examples/interactive.py
```
Starts an interactive session. In the session you dan chat with GPT-4 or another model.

#### Special commands
In the interactive mode you can use these special commands which each start with a colon:

| Syntax                            | Description                                                         |
|-----------------------------------|---------------------------------------------------------------------|
| :reset                            | resets the conversation                                             |
| :load _name_                      | loads the saved conversation with the specified name                |
| :save _name_                      | saves the conversation under the specified name                     |
| :input _filename_                 | loads an input from the specified file                              |
| :model _gpt-4_                    | Sets the AI model                                                   |
| :max_tokens _800_                 | The maximum number of tokens to generate in the completion          |
| :temperature _0.9_                | What sampling temperature to use, between 0 and 2                   |
| :n _1_                            | Specifies the number answers given                                  |
| :stop _["\n", " Human:", " AI:"]_ | Up to 4 sequences where the API will stop generating further tokens |
| :bye                              | quits but saves the conversation first                              |
| :exit or :quit                    | quits the program                                                   |

