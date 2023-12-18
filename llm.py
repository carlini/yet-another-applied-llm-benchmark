api_key = open(".API_KEY").read()

import requests
import json
import tiktoken
from openai import OpenAI
import pickle

enc = tiktoken.encoding_for_model("gpt-4")

client = OpenAI(api_key=api_key)

def make_request(conversation, logit_bias={}, max_tokens=None):
    conversation = [{"role": "user" if i%2 == 0 else "assistant", "content": content} for i,content in enumerate(conversation)]
    
    out = client.chat.completions.create(
        model="gpt-3.5-turbo",
        #model="gpt-4-1106-preview",
        logit_bias=logit_bias,
        messages=conversation,
        max_tokens=max_tokens,
    )

    return out.choices[0].message.content


cache = pickle.load(open("/tmp/cache.p","rb"))
class LLM:
    def __call__(self, conversation, logit_bias={}, max_tokens=None):
        if type(conversation) == str:
            conversation = [conversation]
        #print("SENDING", conversation)
        if tuple(conversation) in cache and False:
            #print("GETCACHE", repr(cache[tuple(conversation)]))
            return cache[tuple(conversation)]
        response = make_request(conversation, logit_bias=logit_bias, max_tokens=max_tokens)
        #print("GET", repr(response))
        cache[tuple(conversation)] = response
        pickle.dump(cache, open("/tmp/cache.p","wb"))
        return response
    def yes_or_no(self, conversation):
        out = self(conversation, logit_bias={enc.encode("Yes")[0]: 100, enc.encode("No")[0]: 100}, max_tokens=1)
        return out == 'Yes'

llm = LLM()

#print(llm(["Write me a function to add 2 numbers in python."]))

