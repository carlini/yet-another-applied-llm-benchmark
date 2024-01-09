import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
from vertexai.preview.generative_models import GenerativeModel


import json
import requests

class VertexAIModel:
    def __init__(self, name):
        self.name = name

        vertexai.init(project="practical-poisoning", location="us-central1")

        if 'gemini' in name:
            self.chat_model = GenerativeModel("gemini-pro")
        else:
            self.chat_model = ChatModel.from_pretrained(name)


    def make_request(self, conversation, add_image=None, logit_bias=None, skip_cache=False, temperature=0.3, top_p=1, max_tokens=2048, stream=False, safe_mode=False, random_seed=None):
        if 'gemini' in self.name:
            response = self.chat_model.generate_content(conversation)
        else:
            conversation_pairs = conversation[:-1]
            conversation_pairs = [(a, b) for a, b in zip(conversation_pairs[::2], conversation_pairs[1::2])]
    
            chat = self.chat_model.start_chat(
                 examples=[
                     InputOutputTextPair(
                         input_text=a,
                         output_text=b,
                     ) for a,b in conversation_pairs]
            )
            response = chat.send_message(
                conversation[-1],
                temperature=temperature, max_output_tokens=max_tokens
            )
        try:
            return response.text
        except:
            return ''
        

if __name__ == "__main__":
    import sys
    #q = sys.stdin.read().strip()
    q = "why?"
    print(VertexAIModel("gemini-pro").make_request(["hi, how are you doing", "i'm a bit sad", q]))
