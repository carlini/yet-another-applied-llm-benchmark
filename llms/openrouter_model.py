
from openai import OpenAI
import json

from llms.openai_model import OpenAIModel


class OpenRouterModel(OpenAIModel):
    def __init__(self, name):
        config = json.load(open("config.json"))
        api_key = config["llms"]["openrouter"]["api_key"].strip()
        self.client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        self.name = name[len("openrouter/") :]
        self.hparams = config["hparams"]
        self.hparams.update(config["llms"]["openrouter"].get("hparams") or {})


if __name__ == "__main__":
    # WARNING: must be run with PYTHONPATH=. otherwise there will be an import error
    # q = sys.stdin.read().strip()
    q = "hello there"
    print(q + ":", OpenRouterModel("openrouter/openai/o1-mini").make_request([q]))
