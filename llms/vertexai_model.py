import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair
from vertexai.preview.generative_models import GenerativeModel


import json
import requests

class VertexAIModel:
    def __init__(self, name):
        self.name = name
        config = json.load(open("config.json"))
        self.hparams = config['hparams']
        self.hparams.update(config['llms']['vertexai'].get('hparams') or {})

        project_id = config['llms']['vertexai']['project_id'].strip()
        vertexai.init(project=project_id, location="us-central1")

        if 'gemini' in name:
            self.chat_model = GenerativeModel(name)
        else:
            self.chat_model = ChatModel.from_pretrained(name)


    def make_request(self, conversation, add_image=None, max_tokens=2048, stream=False):
        if 'gemini' in self.name:
            conversation = [" " if c == "" else c for c in conversation]
            conf = {
                "max_output_tokens": 2048,
              }
            conf.update(self.hparams)
            response = self.chat_model.generate_content(conversation, generation_config=conf)
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
            conf = {
                "max_output_tokens": 2048,
              }
            conf.update(self.hparams)
            response = chat.send_message(
                conversation[-1],
                **conf
            )
        try:
            return response.text
        except:
            return ''
        

if __name__ == "__main__":
    import sys
    #q = sys.stdin.read().strip()
    q = "why?"
    print(VertexAIModel("gemini-1.5-pro-preview-0409").make_request(["hi, how are you doing", "i'm a bit sad", q]))
