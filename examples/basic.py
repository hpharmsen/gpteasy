import sys
sys.path.append('.')
from gpteasy import GPT


if __name__ == "__main__":
    gpt = GPT()
    gpt.model = 'gpt-3.5-turbo' # Optional, the default model is gpt-4
    gpt.system = lambda: "You are a movie critic. I feed you with movie titles and you give me a review in 50 words."

    message = gpt.chat("Forrest Gump")
    print(message.text)
