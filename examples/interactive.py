""" The main chat program to chat with the model"""
import sys
sys.path.append('.')

from gpteasy import GPT, CommandHandler, Repl

if __name__ == "__main__":
    gpt = GPT()
    if len(sys.argv) > 1:  # You can specify the name of a previous conversation to load
        gpt.load(sys.argv[1])

    # Add a command handler that handles special commands like model parameters and system settings
    # Special commands begin with : or /
    # See README.md
    command_handler = CommandHandler(gpt)

    # Start the interactive prompt
    repl = Repl(gpt, command_handler.handle_command)
    repl.show_token_count = True  # Display how many tokens were used in each call
    repl.run()
