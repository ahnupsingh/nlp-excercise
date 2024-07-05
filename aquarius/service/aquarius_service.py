
import json
import pandas as pd
from utils.sentiment_analyzer import ChatGPTSentimentAnalyzer
from aquarius.models import City

class AquariusService:
    def __init__(self):
        self.analyzer = ChatGPTSentimentAnalyzer()

    def get_cities(self):
        cities = City.objects.all()
        return cities

    def get_reviews(self, city):
        data = pd.read_csv('data/amazon_alexa.tsv', sep='\t')
        responses = self.analyzer.analyze_sentiment_in_batch(data)
        self.format_response(responses)

    def format_response(self, responses):
        df_total = pd.DataFrame()
        for response in responses:
            json_data = response.strip("`")
            data = json.loads(json_data)
            df_temp = pd.DataFrame(data)
            df_total = pd.concat([df_total, df_temp], ignore_index=True)

        print(df_total)