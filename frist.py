from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key = api_key,
                base_url = "https://api.deepseek.com")

response = client.chat.completions.create(
    model = "deepseek-v4-pro",
    messages = [{
        "role": "user",
        "content": "你是谁？你能做什么？"
    }])
print(response.choices[0].message.content)
