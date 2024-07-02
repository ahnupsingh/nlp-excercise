from abc import ABC, abstractmethod

class SentimentAnalyzer(ABC):
    """
    An interface for sentiment analysis models.
    """

    @abstractmethod
    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the provided text and return the sentiment score.
        """
        pass