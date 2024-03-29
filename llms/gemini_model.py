import json
import requests

class GeminiModel:
    def __init__(self, name):
        self.name = name
        self.api_key = json.load(open("config.json"))['api_keys']['gemini'].strip()
        self.project_id = json.load(open("config.json"))['llms']['vertexai']['project_id'].strip()
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',  # Adjust if the API expects a different kind of authentication
            'Content-Type': 'application/json'
        }
        self.endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/{name}:streamGenerateContent?alt=sse"

    def make_request(self, conversation, add_image=None, logit_bias=None, skip_cache=False, temperature=0.3, top_p=1, max_tokens=1024, stream=False, safe_mode=False, random_seed=None):
        # Prepare the conversation messages in the required format
        formatted_conversation = [
            {"role": "USER" if i % 2 == 0 else "ASSISTANT", "parts": {'text': content}}
            for i, content in enumerate(conversation)
        ]

        # Construct the data payload
        data = {
          "contents": formatted_conversation,
          "generation_config": {
            "temperature": 0.2,
            "topP": 0.3,
            "topK": 10,
            "maxOutputTokens": 2048,
          }
        }

        # Make the POST request to the API endpoint
        response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(data))
        #print(response.text)
        out = []
        for line in response.text.split("\n"):
            if line.startswith("data:"):
                row = json.loads(line[6:])['candidates'][0]['content']
                if 'parts' in row:
                    out.append(row['parts'][0]['text'])
        return "".join(out)


if __name__ == "__main__":
    import sys
    #q = sys.stdin.read().strip()
    q = "hello there"
    print(GeminiModel("chat-bison").make_request([q]))
