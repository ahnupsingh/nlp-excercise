from .base import SentimentAnalyzer
import time
import openai
from utils.data_preprocessing import clean_text
from django.conf import settings
openai.api_key  = settings.OPENAI_API_KEY

class ChatGPTSentimentAnalyzer(SentimentAnalyzer):

    def __init__(self):
        pass

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
    
    def analyze_sentiment_in_batch(self, data):
        data_balanced = self.prepare_data(data)
        reviews = data_balanced['review'].tolist()
        cleaned_reviews = [clean_text(str(review)) for review in reviews]
        print(cleaned_reviews)

        # Add the cleaned reviews as a new column to the DataFrame
        data_balanced['clean_reviews'] = cleaned_reviews

        # Assuming your DataFrame is called "df"
        total_rows = len(data_balanced)
        test_size = int(total_rows * 0.95)

        # Randomly sample train_size rows for the training set
        test_set = data_balanced.sample(test_size)

        # Get the remaining rows for the test set
        train_set = data_balanced.drop(test_set.index)

        batches = []
        batch_size = 50

        test_set_total = test_set.sample(100)
        test_set_total['pred_label'] = ''

        for i in range(0, len(test_set_total), batch_size):
            batches.append(test_set_total[i : i + batch_size])

        train_sample = train_set.sample(4)
        batch_count = len(batches)
        responses = []
        for i in range(0,len(batches)):
            responses.append(self.gpt_completion_function(batches[i],i,batch_count,train_sample))
        return responses


    def gpt_completion_function(self, batch,current_batch,total_batch,train_sample,model="gpt-3.5-turbo-1106"):
        """Function works in three steps:
        # Step-1: Convert the DataFrame to JSON using the to_json() method.
        # Step-2: Preparing the Gemini Prompt
        # Step-3: Calling GPT API
        """

        json_data = batch[['clean_reviews','pred_label']].to_json(orient='records')
        sample_json_data = train_sample[['clean_reviews','label']].to_json(orient='records')

        prompt = f"""You are an expert linguist, who is good at classifying customer review sentiments into Positive/Negative labels.
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

        print(f"Now processing batch#: {current_batch+1} of {total_batch}")
        json_data = batch[['clean_reviews','pred_label']].to_json(orient='records')
        sample_json_data = train_sample[['clean_reviews','label']].to_json(orient='records')
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(model=model,messages=messages,temperature=0)
        time.sleep(5)
        return response.choices[0].message["content"]

