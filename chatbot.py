import spacy
from spacy.matcher import Matcher
from fuzzywuzzy import fuzz

class ChatBot:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.matcher = Matcher(self.nlp.vocab)
        self.responses = self._load_responses()
        self._add_patterns()

    def _load_responses(self):
        return {
            "greeting": "Hello! How can I help you today?",
            "goodbye": "Goodbye! Have a great day!",
            "freelancer_search": "You can search for freelancers based on skills, experience, and ratings.",
            "job_posting": "To post a job, click on 'Post a Job' and fill in the details.",
            "default": "I'm sorry, I didn't understand that. Could you please rephrase?"
        }

    def _add_patterns(self):
        patterns = {
            "greeting": [{"LOWER": "hello"}, {"LOWER": "hi"}, {"LOWER": "hey"}],
            "goodbye": [{"LOWER": "bye"}, {"LOWER": "goodbye"}, {"LOWER": "see you"}],
            "freelancer_search": [{"LOWER": "find"}, {"LOWER": "freelancer"}],
            "job_posting": [{"LOWER": "post"}, {"LOWER": "job"}]
        }

        for intent, pattern in patterns.items():
            self.matcher.add(intent, [pattern])

    def get_response(self, user_input):
        doc = self.nlp(user_input)
        matches = self.matcher(doc)
        
        if matches:
            match_id, start, end = matches[0]
            intent = self.nlp.vocab.strings[match_id]
            return self.responses.get(intent, self.responses["default"])
        else:
            # Fuzzy matching for greetings
            for word in doc:
                if fuzz.ratio(word.text.lower(), "hello") > 80:
                    return self.responses["greeting"]
                
            return self.responses["default"]
