'''
import pyttsx3#to import the pyttsx3 library in test.py fie

engine=pyttsx3.init()#to return an engine object to use it 


#set the speech rate
rate=engine.getProperty('rate')#to get current speech rate
print(f"current speech rate:{rate}")
engine.setProperty('rate',120)

#set the volume
volume=engine.getProperty('volume')#get the volume level
print(f"current volumelevel:{volume}")
engine.setProperty('volume',0.9)


#set the voice
voices=engine.getProperty('voices')#get the available voices
print(f"current voice is {voices}")
engine.setProperty('voice',voices[0].id)




engine.say("Hey there how are you today?")#to say something like hello

engine.runAndWait()#to run and wait
'''

#speech recogiton

'''
# Define intents and responses
intents = {
    'greeting': ['hello', 'hi', 'hey'],
    'farewell': ['bye', 'goodbye'],
    'gratitude': ['thank you', 'thanks'],
    'query': ['how are you', 'what are you doing'],
    'weather': ['weather', 'temperature', 'forecast'],
    'time': ['time', 'current time'],
    'reminder': ['reminder', 'remind me'],
    'joke': ['joke', 'tell me a joke'],
    'fact': ['fact', 'interesting fact'],
    'meaning': ['meaning of']
}

responses = {
    'greeting': ['Hi there!', 'Hello!', 'Hey!'],
    'farewell': ['Goodbye!', 'See you later!', 'Bye!'],
    'gratitude': ['You\'re welcome!', 'No problem!', 'My pleasure!'],
    'query': ['I\'m doing well, thank you!', 'Just assisting you!', 'Feeling great, thank you for asking!'],
    'weather': ['The weather is sunny today.', 'It\'s cloudy with a chance of rain.'],
    'time': ['The current time is ' + datetime.datetime.now().strftime("%I:%M %p")],
    'reminder': ['Sure, I will remind you.', 'Reminder set successfully.'],
    'joke': ['Why don\'t scientists trust atoms? Because they make up everything!', 'I\'m reading a book on anti-gravity. It\'s impossible to put down!'],
    'fact': ['Did you know that the shortest war in history was between Britain and Zanzibar on August 27, 1896? It lasted only 38 minutes!']
}
'''



#intents in ai assitant
#hello how are you to the ai
#ai:hi i am fine,fine doing,
'''
import random
import datetime

# Define intents and responses
intents = {
    'greeting': ['hello', 'hi', 'hey'],  # Intents for greetings
    'farewell': ['bye', 'goodbye'],  # Intents for farewells
    'gratitude': ['thank you', 'thanks'],  # Intents for expressing gratitude
    'query': ['how are you', 'what are you doing'],  # Intents for asking about the assistant's status
    'weather': ['weather', 'temperature', 'forecast'],  # Intents for weather queries
    'time': ['time', 'current time'],  # Intents for time queries
    'reminder': ['reminder', 'remind me'],  # Intents for setting reminders
    'joke': ['joke', 'tell me a joke'],  # Intents for jokes
    'fact': ['fact', 'interesting fact'],  # Intents for sharing facts
    'meaning': ['meaning of']  # Intents for querying word meanings
}

responses = {
    'greeting': ['Hi there!', 'Hello!', 'Hey!'],  # Responses for greetings
    'farewell': ['Goodbye!', 'See you later!', 'Bye!'],  # Responses for farewells
    'gratitude': ['You\'re welcome!', 'No problem!', 'My pleasure!'],  # Responses for gratitude
    'query': ['I\'m doing well, thank you!', 'Just assisting you!', 'Feeling great, thank you for asking!'],  # Responses for status queries
    'weather': ['The weather is sunny today.', 'It\'s cloudy with a chance of rain.'],  # Responses for weather queries
    'time': ['The current time is ' + datetime.datetime.now().strftime("%I:%M %p")],  # Response for time queries
    'reminder': ['Sure, I will remind you.', 'Reminder set successfully.'],  # Responses for setting reminders
    'joke': ['Why don\'t scientists trust atoms? Because they make up everything!', 'I\'m reading a book on anti-gravity. It\'s impossible to put down!'],  # Responses for jokes
    'fact': ['Did you know that the shortest war in history was between Britain and Zanzibar on August 27, 1896? It lasted only 38 minutes!']  # Response for sharing facts
}

def process_command(command):
    """
    Process the given command and respond appropriately.
    :param command: The user's command.
    """
    found_intent = False
    # Iterate through each intent and its associated keywords
    for intent, keywords in intents.items():
        # Check if any keyword of the intent is in the user's command
        if any(keyword in command.lower() for keyword in keywords):
            found_intent = True
            # Select a random response for the matched intent
            response = random.choice(responses[intent])
            # Print the user's command and the assistant's response
            print(f"User: {command}\nAssistant: {response}\n")
            return
    # If no intent is found, provide a default response
    if not found_intent:
        response = "Sorry, I didn't understand the command."
        print(f"User: {command}\nAssistant: {response}\n")


if __name__ == "__main__":
    # Continuously prompt the user for input until "exit" is entered
    while True:
        user_input = input("You: ")
        # Check if the user wants to exit
        if user_input.lower() == 'exit':
            print("Assistant: Goodbye!")
            break
        # Process the user's command
        process_command(user_input)
        '''
        
        
        
        
        
        
        
        #WAKEUP WORD
        
import speech_recognition as sr

WAKEUP_WORD = "Quagmire"

def listen_for_wakeup_word():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening for wakeup word...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        if WAKEUP_WORD in command:
            print("Wakeup word detected!")
            return True
        else:
            return False
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return False
    except sr.RequestError:
        print("Could not request results. Please check your internet connection.")
        return False

def process_command():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("User:", command)
        # Process the user's command here
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
    except sr.RequestError:
        print("Could not request results. Please check your internet connection.")

# Main loop
while True:
    if listen_for_wakeup_word():
        print("Assistant is now active.")
        process_command()
        

