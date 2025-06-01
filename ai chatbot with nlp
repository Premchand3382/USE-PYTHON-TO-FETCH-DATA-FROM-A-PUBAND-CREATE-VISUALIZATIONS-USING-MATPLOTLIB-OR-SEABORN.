import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Download necessary NLTK data
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Knowledge base: questions and answers
QA_PAIRS = {
    "hello": "Hello! How can I assist you today?",
    "how are you": "I'm a bot, so I am always doing great!",
    "what is your name": "I am your friendly chatbot created using NLTK.",
    "what can you do": "I can answer basic questions. Try asking me something!",
    "bye": "Goodbye! Have a great day!",
    "help": "Sure, I am here to help! You can ask me questions like 'what is your name?' or 'how are you?'.",
    "what is nltk": "NLTK stands for Natural Language Toolkit. It is a popular Python library for working with human language data.",
    "who created you": "I was created by a skilled software engineer using Python and NLTK.",
    "tell me a joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
    "what is ai": "AI stands for Artificial Intelligence, the simulation of human intelligence in machines.",
    "thank you": "You're welcome! Happy to help.",
    "what languages do you speak": "I can understand and respond in English.",
    "can you help me with python": "Absolutely! Feel free to ask me any Python-related questions.",
    "how do you work": "I work by matching your questions with known patterns using natural language processing.",
}

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in stop_words and t not in punctuation]
    return set(tokens)

def find_best_answer(user_input):
    user_tokens = preprocess(user_input)
    best_match = None
    best_score = 0
    for question, answer in QA_PAIRS.items():
        question_tokens = preprocess(question)
        common = user_tokens.intersection(question_tokens)
        score = len(common)
        if score > best_score:
            best_score = score
            best_match = answer
    if best_score == 0:
        return "Sorry, I did not understand your question. Can you please rephrase?"
    else:
        return best_match

def chat():
    print("Welcome to the Chatbot! (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Chatbot: Goodbye! Have a great day!")
            break
        response = find_best_answer(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    chat()


