import requests
import json

class GeminiModel:
    def __init__(self, name):
        self.name = name

        config = json.load(open("config.json"))
        self.api_key = config['llms']['google']['api_key'].strip()

        self.hparams = config['hparams']
        self.hparams.update(config['llms']['openai'].get('hparams') or {})
        
    def make_request(self, conversation, max_tokens=None, add_image=None):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.name}:generateContent?key={self.api_key}"

        contents = []
        for i, content in enumerate(conversation):
            role = "user" if i % 2 == 0 else "model"
            contents.append({"role": role, "parts": [{"text": content}]})

        data = {
            "contents": contents,
            "generationConfig": self.hparams
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        out = response.json()
        print(out)
        return out['candidates'][0]['content']['parts'][0]['text']
    

if __name__ == "__main__":
    q = "Why?"
    model = GeminiModel("gemini-1.5-pro-latest")
    response = model.make_request(["I think 4 is even.", "It is!", "Why?"])
    print(response)

