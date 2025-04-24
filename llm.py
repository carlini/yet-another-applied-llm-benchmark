## Copyright (C) 2024, Nicholas Carlini <nicholas@carlini.com>.
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO
import os
import base64
import requests
import json
import pickle
import time

from llms.openai_model import OpenAIModel
from llms.anthropic_model import AnthropicModel
from llms.mistral_model import MistralModel
from llms.openrouter_model import OpenRouterModel
from llms.vertexai_model import VertexAIModel
from llms.cohere_model import CohereModel
from llms.moonshot_model import MoonshotAIModel
from  llms.groq_model import GroqModel

class LLM:
    def __init__(self, name="gpt-3.5-turbo", use_cache=True, override_hparams={}):
        self.name = name
        if 'openrouter' in name:
            self.model = OpenRouterModel(name)
        elif 'gpt' in name or name.startswith('o1'):
            self.model = OpenAIModel(name)
        # elif 'llama' in name:
        #     self.model = LLAMAModel(name)
        elif 'mistral' in name:
            self.model = MistralModel(name)
        elif 'bison' in name or 'gemini' in name:
            self.model = VertexAIModel(name)
        #elif 'gemini' in name:
        #    self.model = GeminiModel(name)
        elif 'claude' in name:
            self.model = AnthropicModel(name)
        elif 'moonshot' in name:
            self.model = MoonshotAIModel(name)            
        elif 'command' in name:
            self.model = CohereModel(name)
        elif 'llama3' in name or 'mixtral' in name or 'gemma' in name or 'deepseek' in name:
            print("Using Groq model", name)
            self.model = GroqModel(name)
        else:
            raise
        self.model.hparams.update(override_hparams)

        self.use_cache = use_cache
        if use_cache:
            try:
                if not os.path.exists("tmp"):
                    os.mkdir("tmp")
                self.cache = pickle.load(open(f"tmp/cache-{name.split('/')[-1]}.p","rb"))
            except:
                self.cache = {}
        else:
            self.cache = {}

    def __call__(self, conversation, add_image=None, max_tokens=None, skip_cache=False, json=False):
        if type(conversation) == str:
            conversation = [conversation]

        cache_key = tuple(conversation) if add_image is None else tuple(conversation + [add_image.tobytes()])

        if cache_key in self.cache and not skip_cache and self.use_cache:
            
            print(self.name, "GETCACHE", repr(self.cache[cache_key]))
            if len(self.cache[cache_key]) > 0:
                return self.cache[cache_key]
            else:
                print("Empty cache hit")

        print(self.name, "CACHE MISS", repr(conversation))

        
        import traceback
        from concurrent.futures import ThreadPoolExecutor, TimeoutError

        response = "Model API request failed"
        for _ in range(3):
            try:
                extra = {}
                if json:
                    extra['json'] = json
                
                def request_with_timeout():
                    return self.model.make_request(conversation, add_image=add_image, max_tokens=max_tokens, **extra)
                
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(request_with_timeout)
                    try:
                        response = future.result(timeout=60*10)  # 10 minutes
                        break  # If successful, break out of the retry loop
                    except TimeoutError:
                        print("Request timed out after 60 seconds")
                        response = "Model API request failed due to timeout"
                        # Continue to the next retry
            except Exception as e:
                print("RUN FAILED", e)
                traceback.print_exc()
            
            time.sleep(10)
        

        if self.use_cache and response != "Model API request failed":
            self.cache[cache_key] = response
            pickle.dump(self.cache, open(f"tmp/cache-{self.name.split('/')[-1]}.p","wb"))
        
        return response

#llm = LLM("command")
#llm = LLM("gpt-3.5-turbo")
#llm = LLM("gpt-4-turbo-2024-04-09")
#llm = LLM("gemini-1.5-pro-preview-0409")
llm = LLM("o1-mini")

#llm = LLM("claude-3-opus-20240229")
#llm = LLM("claude-3-5-sonnet-20240620")

#llm = LLM("mistral-tiny")
#llm = LLM("gemini-pro", override_hparams={'temperature': 0.3}, use_cache=False)

#eval_llm = LLM("gpt-4-1106-preview")
eval_llm = LLM("gpt-4o", override_hparams={'temperature': 0.1})
#eval_llm = LLM("gpt-3.5-turbo", override_hparams={'temperature': 0.1})

vision_eval_llm = LLM("gpt-4o", override_hparams={'temperature': 0.1})
