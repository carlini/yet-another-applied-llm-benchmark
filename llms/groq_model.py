import groq
import json

class GroqModel:
    def __init__(self, name):
        self.name = name

        config = json.load(open("config.json"))
        self.api_key = config['llms']['groq']['api_key'].strip()

        self.hparams = config['hparams']
        self.hparams.update(config['llms']['groq'].get('hparams') or {})
        
    def make_request(self, conversation, add_image=None, logit_bias=None, max_tokens=None):
        conversation = [{"role": "user" if i%2 == 0 else "assistant", "content": content} for i,content in enumerate(conversation)]
        response = groq.Groq(api_key=self.api_key).chat.completions.create(
            model=self.name,
            max_tokens=2048,
            messages=conversation
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    import sys
    q = "What's your name?"
    print(q+":", GroqModel("llama3-70b-8192").make_request([q]))

