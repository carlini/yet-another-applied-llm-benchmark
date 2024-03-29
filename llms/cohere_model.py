from io import BytesIO
from PIL import Image
import base64

import cohere
import json

class CohereModel:
    def __init__(self, name):
        config = json.load(open("config.json"))
        api_key = config['llms']['cohere']['api_key'].strip()
        self.client = cohere.Client(api_key)
        self.name = name
        self.hparams = config['hparams']
        self.hparams.update(config['llms']['cohere'].get('hparams') or {})

    def make_request(self, conversation, add_image=None, max_tokens=None):
        prior_messages = [{"role": "USER" if i%2 == 0 else "CHATBOT", "message": content} for i,content in enumerate(conversation[:-1])]

        kwargs = {
            "chat_history": prior_messages,
            "message": conversation[-1],
            "max_tokens": max_tokens,
            "model": self.name
        }
        kwargs.update(self.hparams)
    
        for k,v in list(kwargs.items()):
            if v is None:
                del kwargs[k]
    
        out = self.client.chat(
            prompt_truncation='AUTO',
            **kwargs
        )
    
        return out.text

if __name__ == "__main__":
    import sys
    #q = sys.stdin.read().strip()
    q = "what specific date?"
    print(q+":", CohereModel("command").make_request(["Who discovered relativity?", "Einstein.", q]))
