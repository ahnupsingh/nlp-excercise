from abc import ABC, abstractmethod

class Scraper(ABC):
    """
    An interface for Scrapers.
    """

    @abstractmethod
    def scrape(self, text):
        pass