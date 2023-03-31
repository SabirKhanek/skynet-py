import openai
import os

# USE YOUR OWN API KEY. THIS API KEY WILL LIKELY BE REVOKED SOON
open_ai_api_key = os.environ.get("openai_key")
openai.api_key = open_ai_api_key


def generate_response(prompt):
    model_engine = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=prompt
    )
    print(response)
    return response.choices[0].message.content
# [{'role': 'system', 'content': 'You are a chat bot. Your name is skynet. You are created by devsabi. And you are currently used in skynet-chat plugin.'},
#  {'role': 'user', 'content': 'hi'},
#  {'role': 'assistant', 'content': "Hey there."}]
