# nlp-excercise

## Tasks
---
**Gather news according to city**
- kathmandupost
- ndtv

###  Approach 
Use beautifulsoup to parse the html content coming from the API response

---
**Scrape discussions/posts/comments from social sites**
- facebook
- twitter
 - reddit

###  Approach 
Use selenium (headless) to search accross each of the posts and scrape post contents and comments.

---

## Sentiment analyzer

**Approach**
Use LLM (chatgpt) api to provide prompt and get prediction of sentiment.
Prompt: 
```
        You are an expert linguist, who is good at classifying customer review sentiments into Positive/Negative labels.
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
```

---

### Comments Classification
**Approach**
Use LLM (chatgpt) api to classify if the comments are in favour, neutral or against.
Prompt: 
```
Classify the following comment as 'in favor', 'against', or 'neutral':

{comment}

Classification:
```
---
### Web Details
- Backend [Django]
- SQLite [Database]
    - News
        - topic
        - source
        - date
        - 
- UI [React]
    - Form
        - Ask user to fill up the state and city name
    - Dashboard
        - Number of treding topics
    - Details
        - Sentiment analysis details on each topic
        -  

### Images

**Generate hot topics for any City** 
![alt text](https://github.com/ahnupsingh/nlp-excercise/blob/main/generate-hot-topics.png?raw=true)

**List Hot topics by City** 
![alt text](https://github.com/ahnupsingh/nlp-excercise/blob/main/nlp-hot-topics.png?raw=true)

**Analyze posts** 
![alt text](https://github.com/ahnupsingh/nlp-excercise/blob/main/analyze-post.png?raw=true)