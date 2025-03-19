import nltk
from nltk.chat.util import Chat, reflections

# Define chatbot patterns and responses
pairs = [
    [
        r"hi|hello|hey",
        ["Hello!", "Hi there!", "Hey!"]
    ],
    [
        r"how are you?",
        ["I'm doing well, thanks for asking!", "I'm fine, how about you?"]
    ],
    [
        r"what is your name?",
        ["I'm a chatbot created by Python!", "You can call me Chatbot."]
    ],
    [
        r"quit",
        ["Bye! Have a great day ahead.", "Goodbye! Come back soon!"]
    ],
    [
        r"nozzle",
        ["Provide your requirements may i know"]
    ]
]

# Create chatbot
chatbot = Chat(pairs, reflections)

def start_chat():
    print("Hello! I'm your chatbot. Type 'quit' to exit.")
    chatbot.converse()

if __name__ == "__main__":
    start_chat()
