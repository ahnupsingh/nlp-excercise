import json
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

        # TODO : add langchain structured output
        # output_format: json
        # mle-core
        response = openai.ChatCompletion.create(model=self.model,messages=messages,temperature=0)
        time.sleep(5)
        return response.choices[0].message["content"]
    
    def classify_comments(self, post, comment):
        prompt = f"""
        Classify the following comment as 'in favor', 'against', or 'neutral' based on the following post:
        post: {post.topic} - {post.content}
        comment: {comment}
        The final output should be in the following JSON format:
        {{
            "category": "<category>",
            "reason": "<reason>"
        }}
        """
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that classifies comments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150
        )

        content = response.choices[0].message['content'].strip()
        if 'json' in content:
            content = content.split("json\n")[1].replace('`', '').replace('\n', '')

        try:
            classification = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("Response format is incorrect or not JSON parsable.")
        category = classification['category'].strip().lower()
        reason = classification['reason'].strip().lower()
        print(f"Comment: {comment}, Classifiction: {category}, Reason: {reason}")
        return category, reason
    

    def get_hot_topics(self, city, posts):
        post_list = '\n'.join([f"- {post.id} -{post.topic}: {post.content}" for post in posts])
        prompt = f"""
        Identify the hot topic being discussed in the city: {city} out of following posts:
        {post_list}
        Above post is listed in format <post_id> - <post_title>: <post_content>.
        The final output should be in the following JSON format:
        {{
            "<identitfied_hot_topic>": [<post_id>, <post_id>, ...],
        }}
        """
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes popular discussions going around the city."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=150
        )

        content = response.choices[0].message['content'].strip()
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("Response format is incorrect or not JSON parsable.")
        return content
    
    def identify_arguments(self, post, comments):
        comment_list = '\n'.join([f"- {comment.id}-{comment.topic}" for comment in comments])
        prompt = f"""
        Following are the list of comments that are in favour of given post::
        post: {post.topic} - {post.content}

        Comments:
        {comment_list}

        Above post is listed in format <comment_id> - <post_title>: <post_content>.
        Identify the argument used by the customer in the comments to support the post and return it in the following JSON format.

        {{
            "<comment_id>": <argument>
        }}
        """
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes popular discussions going around the city."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=150
        )

        content = response.choices[0].message['content'].strip()
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("Response format is incorrect or not JSON parsable.")
        return content