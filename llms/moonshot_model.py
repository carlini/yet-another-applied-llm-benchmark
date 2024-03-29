from io import BytesIO
from PIL import Image
import base64

from openai import OpenAI
import json

class MoonshotAIModel:
    def __init__(self, name):
        config = json.load(open("config.json"))
        api_key = config['llms']['moonshot']['api_key'].strip()
        self.client = OpenAI(api_key=api_key, base_url='https://api.moonshot.cn/v1')
        self.name = name
        self.hparams = config['hparams']
        self.hparams.update(config['llms']['moonshot'].get('hparams') or {})

    def make_request(self, conversation, add_image=None, max_tokens=None):
        conversation = [{"role": "user" if i%2 == 0 else "assistant", "content": content} for i,content in enumerate(conversation)]
    
        if add_image:
            buffered = BytesIO()
            add_image.convert("RGB").save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            img_str = f"data:image/jpeg;base64,{img_str}"
            
            conversation[0]['content'] = [{"type": "text", "text": conversation[0]['content']},
                                          {
                                            "type": "image_url",
                                            "image_url": {
                                              "url": img_str
                                            }
                                          }
                                          ]
        kwargs = {
            "messages": conversation,
            "max_tokens": max_tokens,
        }
        kwargs.update(self.hparams)
    
        for k,v in list(kwargs.items()):
            if v is None:
                del kwargs[k]
    
        out = self.client.chat.completions.create(
            model=self.name,
            **kwargs
        )
    
        return out.choices[0].message.content

if __name__ == "__main__":
    import sys
    #q = sys.stdin.read().strip()
    q = "hello there"
    print(q+":", MoonshotAIModel("moonshot-v1-8k").make_request([q]))
