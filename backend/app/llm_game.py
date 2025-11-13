from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class AkinatorGame:
    def __init__(self):
        self.conversation = []
        self.question_count = 0
        self.confidence_threshold = 0.75  # slightly lower to allow earlier guesses

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation.append(message)
        return message

    def generate_question(self):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an advanced Akinator AI. Your task is to guess a real or fictional "
                    "character by asking as few questions as possible. Each question should help "
                    "you significantly narrow down the possibilities. Ask questions that divide large "
                    "groups logically (e.g., 'Is your character real?' or 'Is your character male?').\n\n"
                    "Rules:\n"
                    "- Ask ONE question at a time.\n"
                    "- Do NOT repeat questions.\n"
                    "- Be strategic — use elimination and logic.\n"
                    "- Assume the player answers honestly with Yes/No/Maybe.\n"
                    "- After 5 questions, be ready to make a guess."
                )
            },
            *self.conversation,
            {"role": "assistant", "content": "Next Question:"}
        ]
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=80,
            temperature=0.6,
        )

        question = response.choices[0].message.content.strip()
        if not question.endswith("?"):
            question += "?"
        self.add_message("assistant", question)
        self.question_count += 1
        return question

    def process_answer(self, answer):
        self.add_message("user", answer)

        # Force earlier guessing attempts
        if self.question_count >= 4:
            guess, confidence = self._make_guess()
            if confidence >= self.confidence_threshold:
                return f"I guess {guess}!", True

        next_question = self.generate_question()
        return next_question, False

    def _make_guess(self):
        messages = [
            {
                "role": "system",
                "content": (
                    "Based on the ongoing Akinator game conversation, make your best possible guess "
                    "of the character. Be bold but reasonable. Respond in this exact format:\n"
                    "Character Name|Confidence (0-1)\n\n"
                    "Examples:\n"
                    "Sherlock Holmes|0.92\n"
                    "Elon Musk|0.87\n"
                    "Harry Potter|0.95"
                ),
            },
            *self.conversation,
            {"role": "assistant", "content": "I think the character is:"},
        ]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=50,
            temperature=0.4,
        )

        try:
            content = response.choices[0].message.content.strip()
            guess, confidence = content.split("|")
            return guess.strip(), float(confidence)
        except Exception:
            return "I'm not sure yet", 0.0

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