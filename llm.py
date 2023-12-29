api_key = open(".API_KEY").read()

from io import BytesIO
import base64
import requests
import json
import tiktoken
from openai import OpenAI
import pickle
from PIL import Image

enc = tiktoken.encoding_for_model("gpt-4")

client = OpenAI(api_key=api_key)

def make_request(name, conversation, add_image=None, logit_bias=None, max_tokens=None):
    conversation = [{"role": "user" if i%2 == 0 else "assistant", "content": content} for i,content in enumerate(conversation)]
    if add_image:
        buffered = BytesIO()
        add_image.save(buffered, format="JPEG")
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
        "logit_bias": logit_bias,
        "messages": conversation,
        "max_tokens": max_tokens,
    }

    for k,v in list(kwargs.items()):
        if v is None:
            del kwargs[k]

    out = client.chat.completions.create(
        model=name,
        **kwargs
    )

    return out.choices[0].message.content


class LLM:
    def __init__(self, name="gpt-3.5-turbo"):
        self.name = name
        try:
            self.cache = pickle.load(open(f"/tmp/cache-{name}.p","rb"))
        except:
            self.cache = {}

    def __call__(self, conversation, add_image=None, logit_bias=None, max_tokens=None, skip_cache=False):
        if type(conversation) == str:
            conversation = [conversation]
        print("SENDING", conversation)

        cache_key = tuple(conversation) if add_image is None else tuple(conversation + [add_image.tobytes()])
        
        if cache_key in self.cache and not skip_cache:
            print("GETCACHE", repr(self.cache[cache_key]))
            return self.cache[cache_key]
        response = make_request(self.name, conversation, add_image=add_image, logit_bias=logit_bias, max_tokens=max_tokens)
        #print("GET", repr(response))
        self.cache[cache_key] = response
        pickle.dump(self.cache, open(f"/tmp/cache-{self.name}.p","wb"))
        return response

    def yes_or_no(self, conversation):
        out = self(conversation, logit_bias={enc.encode("Yes")[0]: 100, enc.encode("No")[0]: 100}, max_tokens=1)
        return out == 'Yes'

llm = LLM("gpt-3.5-turbo")
eval_llm = LLM("gpt-4-1106-preview")
vision_eval_llm = LLM("gpt-4-vision-preview")
