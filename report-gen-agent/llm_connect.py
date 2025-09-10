import os
import base64
from openai import AzureOpenAI
import json

endpoint = os.getenv("ENDPOINT_URL", "https://aihac-mfc0kjaa-eastus2.cognitiveservices.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-5-chat")
subscription_key = "<ffs just let me push this ffs>"

chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that gets RFI data from a database and provides answers about defence RFI bids."
            }
        ]
    },
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "Make sure your answers are no longer than 200 words."
            }
        ]
    }
]

class LLMConnect:
    def __init__(self):
        self.client = AzureOpenAI(
            api_version="2025-01-01-preview",
            azure_endpoint=endpoint,
            api_key=subscription_key,
        )

    def send_prompt(self, prompt):

        chat_prompt.append(prompt)

        completion = self.client.chat.completions.create(
            model=deployment,
            messages=chat_prompt,
            max_completion_tokens=800,
            stop=None,
            stream=False
        )

        return completion.to_json()



### prompt should look like this
# {
#     "role": "user",
#     "content": [
#         {
#             "type": "text",
#             "text": "I am going to Paris, what should I see?"
#         }
#     ]
# }


if __name__ == "__main__":
    llm = LLMConnect()
    user_prompt = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What do you know about defence RFI bids?"
            }
        ]
    }
    theanswer = llm.send_prompt(user_prompt)
    answer_obj = json.loads(theanswer)
    print(answer_obj["choices"][0]["message"]['content'])

