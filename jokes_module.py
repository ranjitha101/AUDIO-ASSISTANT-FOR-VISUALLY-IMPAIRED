import pyttsx3
import random

def tell_joke():
    jokes = [
        "Why did the computer get cold? Because it forgot to close its windows.",
        "Why don’t robots ever panic? They have nerves of steel.",
        "What did the keyboard say to the computer? You are just my type.",
    ]
    joke = random.choice(jokes)
    engine = pyttsx3.init()
    engine.say(joke)
    engine.runAndWait()
