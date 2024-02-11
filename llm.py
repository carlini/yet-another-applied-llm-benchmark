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

from llms.openai_model import OpenAIModel
from llms.anthropic_model import AnthropicModel
from llms.mistral_model import MistralModel
from llms.vertexai_model import VertexAIModel
from llms.cohere_model import CohereModel

class LLM:
    def __init__(self, name="gpt-3.5-turbo", use_cache=True, override_hparams={}):
        self.name = name
        if 'gpt' in name:
            self.model = OpenAIModel(name)
        elif 'llama' in name:
            self.model = LLAMAModel(name)
        elif 'mistral' in name:
            self.model = MistralModel(name)
        elif 'gemini' in name or 'bison' in name:
            self.model = VertexAIModel(name)
        elif 'claude' in name:
            self.model = AnthropicModel(name)
        elif 'command' in name:
            self.model = CohereModel(name)
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

    def __call__(self, conversation, add_image=None, max_tokens=None, skip_cache=False):
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

        response = "Model API request failed"
        for _ in range(3):
            try:
                response = self.model.make_request(conversation, add_image=add_image, max_tokens=max_tokens)
            except:
                pass
        

        if self.use_cache and response != "Model API request failed":
            self.cache[cache_key] = response
            pickle.dump(self.cache, open(f"tmp/cache-{self.name.split('/')[-1]}.p","wb"))
        
        return response

#llm = LLM("command")
#llm = LLM("gpt-3.5-turbo")
#llm = LLM("gpt-4-1106-preview")
llm = LLM("claude-instant-1.2")
#llm = LLM("mistral-tiny")
#llm = LLM("gemini-pro", override_hparams={'temperature': 1.0}, use_cache=False)

#eval_llm = LLM("gpt-4-1106-preview")
eval_llm = LLM("gpt-4-0125-preview", override_hparams={'temperature': 0.1})
#eval_llm = LLM("gpt-3.5-turbo", override_hparams={'temperature': 0.1})

vision_eval_llm = LLM("gpt-4-vision-preview", override_hparams={'temperature': 0.1})
