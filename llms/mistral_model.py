import json
import time
import requests

class MistralModel:
    def __init__(self, name):
        self.name = name
        self.api_key = json.load(open("config.json"))['llms']['mistral']['api_key'].strip()
    
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',  # Adjust if the API expects a different kind of authentication
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.endpoint = "https://api.mistral.ai/v1/chat/completions"

    def make_request(self, conversation, add_image=None, logit_bias=None, skip_cache=False, temperature=0.3, top_p=1, max_tokens=None):
        # Prepare the conversation messages in the required format
        formatted_conversation = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": content}
            for i, content in enumerate(conversation)
        ]

        # Construct the data payload
        data = {
            "model": self.name,  # Update with the desired model name as needed
            "messages": formatted_conversation,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens or 2048,
        }

        # Make the POST request to the API endpoint
        response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(data))
        time.sleep(1)
        if response.status_code == 200:
            # Parse and return the response content
            return response.json()['choices'][0]['message']['content']
        else:
            # Handle errors or unsuccessful status codes as needed
            return f"API request failed with status code {response.status_code}"

if __name__ == "__main__":
    import sys
    q = sys.stdin.read().strip()
    print(q+":", MistralModel("mistral-small").make_request([q]))
