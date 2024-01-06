import anthropic

class ClaudeModel:
    def __init__(self, name):
        self.name = name
        self.api_key = open(".CLAUDE_API_KEY").read()

    def make_request(self, conversation, add_image=None, logit_bias=None, max_tokens=None):
        conversation = [{"role": "user" if i%2 == 0 else "assistant", "content": content} for i,content in enumerate(conversation)]
        response = anthropic.Anthropic().beta.messages.create(
            model=self.name,
            max_tokens=2048,
            messages=[
                conversation
            ]
        )

        return out.content[0].text
