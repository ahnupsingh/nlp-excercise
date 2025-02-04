import openai

from dotenv import dotenv_values
config = dotenv_values(".env") 

OPENAI_API_KEY=config.get('OPENAI_API_KEY')
openai.api_key  = OPENAI_API_KEY

def get_completion(prompt, model="gpt-3.5-turbo-1106"):

  messages = [{"role": "user", "content": prompt}]
  response = openai.ChatCompletion.create(model=model,messages=messages,temperature=0)

  return response.choices[0].message["content"]

get_completion("Hello, how are you today?")