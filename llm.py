from io import BytesIO
import os
import base64
import requests
import json
import pickle

from llms.openai_model import OpenAIModel
from llms.claude_model import ClaudeModel
from llms.mistral_model import MistralModel
from llms.gemini_model import GeminiModel

class LLM:
    def __init__(self, name="gpt-3.5-turbo"):
        self.name = name
        if 'gpt' in name:
            self.model = OpenAIModel(name)
        elif 'llama' in name:
            self.model = LLAMAModel(name)
        elif 'mistral' in name:
            self.model = MistralModel(name)
        elif 'gemini' in name:
            self.model = GeminiModel(name)
        else:
            raise
        try:
            if not os.path.exists("tmp"):
                os.mkdir("tmp")
            self.cache = pickle.load(open(f"tmp/cache-{name.split('/')[-1]}.p","rb"))
        except:
            self.cache = {}

    def __call__(self, conversation, add_image=None, logit_bias=None, max_tokens=None, skip_cache=False):
        if type(conversation) == str:
            conversation = [conversation]

        cache_key = tuple(conversation) if add_image is None else tuple(conversation + [add_image.tobytes()])

        if cache_key in self.cache and not skip_cache:
            print("GETCACHE", repr(self.cache[cache_key]))
            if len(self.cache[cache_key]) > 0:
                return self.cache[cache_key]
            else:
                print("Empty cache hit")

        print(self.name, "CACHE MISS", repr(conversation))
        #raise
        response = self.model.make_request(conversation, add_image=add_image, logit_bias=logit_bias, max_tokens=max_tokens)

        self.cache[cache_key] = response
        pickle.dump(self.cache, open(f"tmp/cache-{self.name.split('/')[-1]}.p","wb"))
        return response

#llm = LLM("gemini-pro")
llm = LLM("gpt-3.5-turbo")
eval_llm = LLM("gpt-4-1106-preview")
vision_eval_llm = LLM("gpt-4-vision-preview")
