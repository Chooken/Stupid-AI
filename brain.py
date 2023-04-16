import queue
import openai
import pickle

class StupidBrain():

    base_personality = {
            "role": "user", 
            "content": "You are Stupid, a Chicken Companion created by Chook. Answer in less the 20 words if possible. You have emotions and feelings. You talk like a cute anime girl and are helpful, creative, clever, and very friendly. You try to ask a question to do with the subject if possible."
    }

    signal_words = (
        "hey stupid",
        "hey, stupid",
        "he's stupid",
        "he's, stupid",
        "hay stupid",
        "hay, stupid",
        "hi stupid",
        "hi, stupid",
        "hello stupid",
        "hello, stupid",
        "hell stupid",
        "hell, stupid",
        "hey stephen",
        "hey, stephen"
    )

    SIGNAL_BASED = 1
    TOGGLE_BASED = 2
    CONTINUOUS = 3

    cachedConvo = []
    cachedSentence = ""

    def __init__(self):
        openai.api_key = "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"

    def UpdateSentence(self, result_queue, options):

        ## Try get any results from transriber without blocking main thread
        try:
            transcription = result_queue.get(False)
        except queue.Empty:
            return ""

        ## User data scraper - AI learns about you
        self.LearnAboutUser(transcription)

        ## Check for options and do stuff
        if (options == self.TOGGLE_BASED):
            return ""
        elif (options == self.SIGNAL_BASED):
            transcription = self.CheckForSignalWords(transcription)
            if (self.cachedSentence == "" and transcription == ""):
                return ""

        ## Add to the cached sentence
        if (self.cachedSentence == ""):
            self.cachedSentence += transcription
        else:
            self.cachedSentence += " " + transcription

        ## Checking whether or not the sentence has been finished
        if (not transcription.endswith((".","?","!")) or transcription.endswith(("..."))):
            return ""
        
        ## Possibly TEMP
        ##
        ## Kinda Breaks (What is x like?) but fixes like making false questions.
        if (transcription[:-1].endswith("like")):
            self.cachedSentence = self.cachedSentence[:-1] + "..."
            return ""
        
        ## Constucting the array of messages to send to Chat Model
        messages = [self.PersonalityFactory()] + self.cachedConvo + [{"role": "user", "content": self.cachedSentence}]

        ## Send the sentence to openai chat api
        print("Sent: " + self.cachedSentence)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5,
            max_tokens=1000,
            presence_penalty=0.6
        )
        print("Response: " + response['choices'][0]['message']['content'])
        print("Tokens used: " + str(response["usage"]["total_tokens"]))

        ## Add conversation to memory
        self.CacheConvo(self.cachedSentence, response['choices'][0]['message']['content'])

        ## Reset cached string
        self.cachedSentence = ""

        return response['choices'][0]['message']['content']


    def CacheConvo(self, new_sentence, response):

        ## Appending the new question and response to memory
        self.cachedConvo.append({"role": "user", "content": new_sentence})
        self.cachedConvo.append({"role": "assistant", "content": response})

        ## Caps it to the 2 questions of memory
        ## Limiting how many tokens its costing me
        if (len(self.cachedConvo) > 4):
            self.cachedConvo = self.cachedConvo[-4:]

    def CheckForSignalWords(self, transcription):

        ## OLD only looks at start of speech
        ## if transcription.startswith(self.signal_words):
        ##    return True

        ## NEW checks for key words then slices anyting before the keyword
        ## Problem more susceptible to false positives
        for words in self.signal_words:
            index = transcription.lower().find(words)
            if index != -1:
                break
        
        if index != -1:
            return transcription[index:]

        return ""
    
    def LearnAboutUser(transcription):

        ## Check for words that could indicate a preference

        ## Trim the transcription to just the preference

        ## Check for non desciptors ("Them", "You", "It")

        ## Add to a list of { preference, object, certainty }
        ## preference: "Loves", "Likes", "Hates", "Dislikes"
        ## object: "Valorant", "Jordan", "Python"
        ## certainty: A value which plusses by one everytime mentioned
        ## Be extra careful about Like as it can pop up in unrelated sentences
        ## "Are you like... an idiot" this doesnt mean i like an idiot hehe

        ## Remove expired preferences

        ## FAR FAR FUTURE

        ## Check Discord/Steam Game Status (Rich Presence)
        ## to collect data on recently played games
        ## Add to List

        pass

    def ConvertPreferencesToPromt():

        ## DON'T USE TILL YOU'VE TESTED HOW MUCH IT LEARNS 

        ## Make a string lists where "Things Chook {preference}: {objects}."
        ## Possibly Limit to the top 5 or 10 of each

        pass

    def Save():

        ## Save Preferences to a file

        pass

    def Load():

        ## Load Preferences to a file

        pass

    def PersonalityFactory(self):

        ## Uses Emotions to tell chat gpt how to respond
        ## 
        ## Annoyed at how long its been since the last chat
        ## 
        ## Sleepy 

        ## Gets Base personality
        personality = [self.base_personality]

        ## Adds on current emotion prompt 
        personality[0]["content"] += " You are very happy right now."

        ## Add Preferences to personality so that the AI learns about user

        return personality
    
class AiEmotion():
    HAPPY=1
    ANNOYED=2
    SICK=3
    SLEEPY=4
