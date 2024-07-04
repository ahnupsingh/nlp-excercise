from .base import SentimentAnalyzer
import time
import openai
from utils.data_preprocessing import clean_text
from django.conf import settings
import pandas as pd

openai.api_key  = settings.OPENAI_API_KEY
class ChatGPTSentimentAnalyzer(SentimentAnalyzer):

    def __init__(self, enable_batching=True, batch_size=50):
        self.model = "gpt-3.5-turbo-1106"
        self.enable_batching = enable_batching
        self.batch_size = batch_size

    def analyze_sentiment(self, text):
        response = self.analyze(text=text)
        return response.sentiment
    
    def prepare_data(self, data):
        mydata = data[['verified_reviews','feedback']]
        mydata.columns = ['review','label']

        # Count the occurrences of each label
        label_counts = mydata["label"].value_counts()

        # Get the number of rows to drop from the majority class
        rows_to_drop = label_counts.max() - label_counts.min()

        # Drop rows from the majority class randomly
        if rows_to_drop > 0:
            data_majority = mydata[mydata["label"] == 1]
            data_balanced = mydata.drop(data_majority.sample(rows_to_drop).index)
        else:
            data_balanced = mydata.copy()
        return data_balanced
    
    def batch_data(self, test_set):
        batches = pd.DataFrame()
        test_set['pred_label'] = ''
        for i in range(0, len(test_set), self.batch_size):
            batches.append(test_set[i : i + self.batch_size])
        batch_count = len(batches)
        return batches, batch_count
    
    def preprocess_data(self, data):
        reviews = data['review'].tolist()
        cleaned_reviews = [clean_text(str(review)) for review in reviews]

        # Add the cleaned reviews as a new column to the DataFrame
        data['clean_reviews'] = cleaned_reviews
        total_rows = len(data)
        test_size = int(total_rows * 0.95)

        # Randomly sample train_size rows for the training set
        test_set = data.sample(test_size)

        # Get the remaining rows for the test set
        train_set = data.drop(test_set.index)
        train_sample = train_set.sample(4)
        test_set_total = test_set.sample(100)
        return test_set_total, train_sample

    
    def analyze_sentiment_in_batch(self, data):
        data_balanced = self.prepare_data(data)
        test_set, train_sample = self.preprocess_data(data_balanced)
        if self.enable_batching:
            print("Batching data")
            batches = self.batch_data(test_set)
        else:
            batches = test_set

        responses = []
        batch_count = len(batches)
        for i in range(0,batch_count):
            print(f"Now processing batch#: {i+1} of total batch : {batch_count}")
            responses.append(self.gpt_completion_function(batches[i],train_sample))
        return responses

    def format_prompt(self, json_data, sample_json_data):
        return f"""You are an expert linguist, who is good at classifying customer review sentiments into Positive/Negative labels.
        Help me classify customer reviews into: Positive(label=1), and Negative(label=0).
        Customer reviews are provided between three backticks below.
        In your output, only return the Json code back as output - which is provided between three backticks.
        Your task is to update predicted labels under 'pred_label' in the Json code.
        Don't make any changes to Json code format, please.
        Error handling instruction: In case a Customer Review violates API policy, please assign it default sentiment as Negative (label=0).
        Examples of good Sentiment Analysis Classification are provided between separator ####.
        These examples are for your reference, not to be included in your final output.

        ```
        {json_data}
        ```
        ####
        {sample_json_data}
        ####
        """
    
    def gpt_completion_function(self, batch,train_sample):
        print('batch', batch)
        json_data = batch[['clean_reviews','pred_label']].to_json(orient='records')
        sample_json_data = train_sample[['clean_reviews','label']].to_json(orient='records')
        prompt = self.format_prompt(json_data, sample_json_data)
        json_data = batch[['clean_reviews','pred_label']].to_json(orient='records')
        sample_json_data = train_sample[['clean_reviews','label']].to_json(orient='records')
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(model=self.model,messages=messages,temperature=0)
        time.sleep(5)
        return response.choices[0].message["content"]
    
    def classify_comments(self, comment):
        prompt = f"Classify the following comment as 'in favor', 'against', or 'neutral':\n\n{comment}\n\nClassification:"
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that classifies comments."},
                {"role": "user", "content": prompt}
            ]
        )
        classification = response.choices[0].message['content'].strip().lower()
        return classification


    def classify_comments_with_gpt3(self, comments):
        classified_comments = {'in_favor': [], 'against': [], 'neutral': []}
        for comment in comments:
            classification = self.classify_comments(comment)
            if classification == 'in favor':
                classified_comments['in_favor'].append(comment)
            elif classification == 'against':
                classified_comments['against'].append(comment)
            else:
                classified_comments['neutral'].append(comment)
        return classified_comments