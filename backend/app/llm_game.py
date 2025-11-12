from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class AkinatorGame:
    def __init__(self):
        self.conversation = []
        self.question_count = 0
        self.confidence_threshold = 0.8

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation.append(message)
        return message

    def generate_question(self):
        messages = [
            {
                "role": "system", 
                "content": """You are playing a game of 20 questions to guess a character.
                Ask one clear, specific question at a time to narrow down the possibilities.
                Your questions should be answerable with Yes/No/Maybe."""
            },
            *self.conversation,
            {"role": "assistant", "content": "Question: "}
        ]
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=100,
            temperature=0.7,
            stop=["\n"]
        )
        
        question = response.choices[0].message.content.strip()
        self.add_message("assistant", question)
        self.question_count += 1
        return question

    def process_answer(self, answer):
        self.add_message("user", answer)
        
        if self.question_count >= 5:
            guess, confidence = self._make_guess()
            if confidence >= self.confidence_threshold:
                return guess, True
        
        next_question = self.generate_question()
        return next_question, False

    def _make_guess(self):
        messages = [
            {
                "role": "system", 
                "content": """Guess the character based on the conversation.
                Respond in format: Character Name|Confidence (0-1)
                Example: Sherlock Holmes|0.9"""
            },
            *self.conversation,
            {"role": "assistant", "content": "I think the character is: "}
        ]
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=50,
            temperature=0.3
        )
        
        try:
            guess, confidence = response.choices[0].message.content.split('|')
            return guess.strip(), float(confidence)
        except:
            return "I'm not sure who you're thinking of.", 0.0

    def to_dict(self):
        return {
            "conversation": self.conversation,
            "question_count": self.question_count
        }

    @classmethod
    def from_dict(cls, data):
        game = cls()
        game.conversation = data["conversation"]
        game.question_count = data["question_count"]
        return game