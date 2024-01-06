from llama_cpp import Llama


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
