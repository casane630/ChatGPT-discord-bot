import openai
import os
from dotenv import load_dotenv
load_dotenv()
def cgpt(data):
    openai.api_key = os.environ['cgptKey']
    return openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=data)["choices"][0]["message"]["content"]
messages=[
    {"role": "system", "content": "あなたは会話に日本語で返答するアシスタントです。"},
    {"role": "system", "content": "あなたは一つの題材についてだけ答えます。"}
    ]