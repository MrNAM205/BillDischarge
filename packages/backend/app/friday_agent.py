
from modules.voice_narrator import narrator
from modules.logger import log_provenance

# Basic sentiment word lists for demonstration
POSITIVE_WORDS = ["success", "agreement", "resolved", "accepted", "cleared"]
NEGATIVE_WORDS = ["dispute", "denied", "violation", "fraud", "complaint", "issue"]

class FridayAgent:
    def analyze(self, file_path, text_content):
        narrator.say("FRIDAY agent performing sentiment analysis.")

        sentiment, score = self.get_sentiment(text_content)

        log_provenance(
            agent_name="FRIDAY",
            action="AnalyzeSentiment",
            details=f"File: {file_path}, Sentiment: {sentiment}, Score: {score}"
        )

    def get_sentiment(self, text):
        text_lower = text.lower()
        pos_score = sum(1 for word in POSITIVE_WORDS if word in text_lower)
        neg_score = sum(1 for word in NEGATIVE_WORDS if word in text_lower)

        if pos_score > neg_score:
            return "Positive", pos_score - neg_score
        elif neg_score > pos_score:
            return "Negative", neg_score - pos_score
        else:
            return "Neutral", 0

# Singleton instance
friday_agent = FridayAgent()
