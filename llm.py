from io import BytesIO
import base64
import requests
import json
from openai import OpenAI
import pickle
from PIL import Image

from llama_cpp import Llama

class OpenAIModel:
    def __init__(self, name):
        api_key = open(".OPENAI_API_KEY").read().strip()
        self.client = OpenAI(api_key=api_key)
        self.name = name

    def make_request(self, conversation, add_image=None, logit_bias=None, max_tokens=None):
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
            "logit_bias": logit_bias,
            "messages": conversation,
            "max_tokens": max_tokens,
        }
    
        for k,v in list(kwargs.items()):
            if v is None:
                del kwargs[k]
    
        out = self.client.chat.completions.create(
            model=self.name,
            **kwargs
        )
    
        return out.choices[0].message.content

class ClaudeModel:
    def __init__(self, name):
        self.api_key = open(".CLAUDE_API_KEY").read()

    def make_request(self, conversation, add_image=None, logit_bias=None, max_tokens=None):
        conversation = [{"role": "user" if i%2 == 0 else "assistant", "content": content} for i,content in enumerate(conversation)]
        response = anthropic.Anthropic().beta.messages.create(
            #model="claude-2.1",
            model = "claude-instant-1.2",
            max_tokens=1024,
            messages=[
                conversation
            ]
        )

        return out.content[0].text

class LLAMAModel:
    def __init__(self, path):
        self.llm = Llama(model_path=path, chat_format="llama-2", n_ctx=1524)

    def make_request(self, conversation, add_image=None, logit_bias=None, max_tokens=None, skip_cache=False):
        conversation = [{"role": "user" if i%2 == 0 else "assistant", "content": content} for i,content in enumerate(conversation)]
        print("Start chat")
        out = self.llm.create_chat_completion(
          messages = conversation
            )
        print("End chat")
        return out['choices'][0]['message']['content']

import json
import requests

class MistralModel:
    def __init__(self, name):
        self.name = name
        self.api_key = open(".MISTRAL_API_KEY").read().strip()  # Ensure to securely store and access your API key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',  # Adjust if the API expects a different kind of authentication
            'Content-Type': 'application/json'
        }
        self.endpoint = "https://api.mistral.ai/v1/chat/completions"

    def make_request(self, conversation, add_image=None, logit_bias=None, skip_cache=False, temperature=0.3, top_p=1, max_tokens=1024, stream=False, safe_mode=False, random_seed=None):
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
            "max_tokens": max_tokens or 1024,
            "stream": stream,
            "safe_mode": safe_mode,
            "random_seed": random_seed
        }

        # Make the POST request to the API endpoint
        response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            # Parse and return the response content
            return response.json()['choices'][0]['message']['content']
        else:
            # Handle errors or unsuccessful status codes as needed
            return f"API request failed with status code {response.status_code}"

        
class LLM:
    def __init__(self, name="gpt-3.5-turbo"):
        self.name = name
        if 'gpt' in name:
            self.model = OpenAIModel(name)
        elif 'llama' in name:
            self.model = LLAMAModel(name)
        elif 'mistral' in name:
            self.model = MistralModel(name)
        else:
            raise
        try:
            self.cache = pickle.load(open(f"/tmp/cache-{name.split('/')[-1]}.p","rb"))
        except:
            self.cache = {}

    def __call__(self, conversation, add_image=None, logit_bias=None, max_tokens=None, skip_cache=False):
        if type(conversation) == str:
            conversation = [conversation]

        cache_key = tuple(conversation) if add_image is None else tuple(conversation + [add_image.tobytes()])

        if cache_key in self.cache and not skip_cache:
            print("GETCACHE", repr(self.cache[cache_key]))
            return self.cache[cache_key]

        response = self.model.make_request(conversation, add_image=add_image, logit_bias=logit_bias, max_tokens=max_tokens)

        self.cache[cache_key] = response
        pickle.dump(self.cache, open(f"/tmp/cache-{self.name.split('/')[-1]}.p","wb"))
        return response

#llm = LLM("/Users/Nicholas/Downloads/llama-2-13b-chat.Q4_K_M.gguf")
#llm = LLM("mistral-tiny")
#print(llm(["What is 5+6?"], skip_cache=True))
#exit(0)
    
llm = LLM("gpt-3.5-turbo")
eval_llm = LLM("gpt-4-1106-preview")
vision_eval_llm = LLM("gpt-4-vision-preview")
