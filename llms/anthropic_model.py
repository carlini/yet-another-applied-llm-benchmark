import anthropic
import json

class AnthropicModel:
    def __init__(self, name):
        self.name = name

        config = json.load(open("config.json"))
        self.api_key = config['llms']['anthropic']['api_key'].strip()

        self.hparams = config['hparams']
        self.hparams.update(config['llms']['anthropic'].get('hparams') or {})
        
    def make_request(self, conversation, add_image=None, logit_bias=None, max_tokens=None):
        conversation = [{"role": "user" if i%2 == 0 else "assistant", "content": content} for i,content in enumerate(conversation)]
        response = anthropic.Anthropic(api_key=self.api_key).messages.create(
            model=self.name,
            max_tokens=2048,
            messages=conversation
        )

        return response.content[0].text


if __name__ == "__main__":
    import sys
    q = "What's your name?"
    print(q+":", AnthropicModel("claude-3-5-sonnet-20240620").make_request([q]))

