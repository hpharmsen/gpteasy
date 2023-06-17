import sys
sys.path.append('.')
from gpteasy import GPT


if __name__ == "__main__":
    gpt = GPT()
    gpt.model = 'gpt-3.5-turbo'

    message = gpt.chat("Tell me about yourself.")
    print(message.text)
