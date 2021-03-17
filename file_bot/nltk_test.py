import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

from nltk.chat.util import Chat, reflections

from io import StringIO
import sys

flag = True

set_pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you doing today ?",]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ], 
    [
        r"what is your name?",
        ["You can call me a chatbot ?",]
    ],
    [
        r"how are you ?",
        ["I am fine, thank you! How can i help you?",]
    ],
    [
        r"I am fine, thank you",
        ["great to hear that, how can i help you?",]
    ],
    [
        r"how can i help you? ",
        ["It is my function to help you.", "I just want to fulfill my purpose",]
    ],
    [
        r"i'm doing good",
        ["That's great to hear","How can i help you?:)",]
    ],
    [
        r"(.*) thank you so much, that was helpful",
        ["I am happy to help", "No problem, you're welcome",]
    ],
    [
        r"quit",
    ["Bye, take care. See you soon :) ","It was nice talking to you. See you soon :)"]
],
]

f = open(r"/Users/keerthanamadhavan/Automation_Python/file_bot", 'r', errors='ignore')
raw = f.read()
raw = raw.lower()

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()
#WordNet is a semantically-oriented dictionary of English included in NLTK.
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
     
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def chatbot():
        
        chat = Chat(set_pairs, reflections)
        
        user_input = quit
        try:
                user_input = input(">")
        except EOFError:
                print(user_input)
        if user_input:
        
                user_input = user_input[:-1]
                if chat.respond(user_input) != None:
                        print(chat.respond(user_input))
                else:
                        user_response = user_input
                        user_response=user_response.lower()
                        if(user_response!='bye'):
                                if(user_response=='thanks' or user_response=='thank you'):
                                        flag=False
                                        print("Bot: You are welcome..")
                                else:
                                        if(greeting(user_response)!= None):
                                                print("Bot: "+greeting(user_response))
                                        else:
                                           
                                            if("python" in user_response):
                                                print("Bot: ",end="")
                                                print(response(user_response))
                                                sent_tokens.remove(user_response)
                                            elif("combine" and "file" in user_response):
                                                for i in range(100):
                                                    print ("\n")
                                                print("Entering file combining mode. Please enter the exact directory we will be combining.")
                                                directory = input(">")
                                                os.chdir(directory)
                                                print("Thank you. Now please enter keyword to identify target files by title:")
                                                keyword = input(">")
                                                reg_pattern = r'(.*'+keyword+'.+\.pdf)|(^'+keyword+'_.*\.pdf)|(.*_'+keyword+'\.pdf)|(.*'+keyword+'.+\.pdf)'
                                                #  instantiate a bot object, I call it bot1 here
                                                bot1 = combine_pdf.FileBots(directory, reg_pattern)
                                                #  use the .locate method to find files of interest
                                                bot1.locate(show=True)
                                                bot1.pdf_merge_tree()
                                            else:
                                                print("Bot: ",end="")
                                                print(wq.chatbot_query(user_response))
                        else:
                                flag=False
                                print("Bot: Bye! take care..")
        #reply = chat.respond()
##        old_stdout = sys.stdout
##        sys.stdout = mystdout = StringIO()
##        sys.stdout = old_stdout
##        print('farts',mystdout.getvalue())






def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        
        return None
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response



if __name__ == "__main__":
        start=True
        
        while flag == True:
                if start==True:
                        print("Hi, I'm your automated assistant")
                        start=False
                chatbot()