import kagglehub
import os
import torch
import json

# !git clone https://github.com/google/gemma_pytorch.git
# !pip install -q -U torch immutabledict sentencepiece
import sys

sys.path.append("gemma_pytorch")  # @TODO make it cleaner
from gemma_pytorch.gemma.config import get_config_for_7b, get_config_for_2b
from gemma_pytorch.gemma.model import GemmaForCausalLM


class GemmaModel:
    def __init__(self, variant, machine_type="cuda"):
        """
        Request models access at https://www.kaggle.com/models/google/gemma/frameworks/pyTorch
        Generate API token for kaggle
        
        Do `git clone https://github.com/google/gemma_pytorch.git` This is required for now. 
        Tested on colab and the test succeeded 
        !PYTHONPATH='.' python tests/print_hello.py
        !PYTHONPATH='.' python tests/explain_code_prime.py
        Unlike other models, Gemma doesnt require any paid account or any other setup.
        Adds much more flexible to add new test cases and run them.
        """
        # variant format : 'gemma:2b-it', 'gemma:7b-it'
        self.variant = variant.split(":")[-1]
        self.machine_type = machine_type
        self.weights_dir = None
        self.tokenizer_path = None
        self.ckpt_path = None
        self.model = None
        self.login()
        self.choose_variant_and_machine()
        self.load_model()
        config = json.load(open("config.json"))
        self.hparams = config["hparams"]
        self.hparams.update(config["llms"]["gemma"].get("hparams") or {})

    def login(self):
        config = json.load(open("config.json"))
        os.environ["KAGGLE_USERNAME"] = config["llms"]["gemma"][
            "KAGGLE_USERNAME"
        ].strip()
        os.environ["KAGGLE_KEY"] = config["llms"]["gemma"]["KAGGLE_KEY"].strip()

    def choose_variant_and_machine(self):
        self.weights_dir = kagglehub.model_download(
            f"google/gemma/pyTorch/{self.variant}"
        )
        self.tokenizer_path = os.path.join(self.weights_dir, "tokenizer.model")
        assert os.path.isfile(self.tokenizer_path), "Tokenizer not found!"
        self.ckpt_path = os.path.join(self.weights_dir, f"gemma-{self.variant}.ckpt")
        assert os.path.isfile(self.ckpt_path), "PyTorch checkpoint not found!"

    def load_model(self):
        assert (
            self.weights_dir is not None
        ), "Weights directory is not set. Call choose_variant_and_machine() first."
        model_config = (
            get_config_for_2b() if "2b" in self.variant else get_config_for_7b()
        )
        model_config.tokenizer = self.tokenizer_path
        model_config.quant = "quant" in self.variant
        torch.set_default_dtype(model_config.get_dtype())
        device = torch.device(self.machine_type)
        self.model = GemmaForCausalLM(model_config)
        self.model.load_weights(self.ckpt_path)
        self.model = self.model.to(device).eval()

    def generate_sample(self, prompt, output_len=60):
        assert self.model is not None, "Model is not loaded. Call load_model() first."
        return self.model.generate(
            prompt, device=torch.device(self.machine_type), output_len=output_len
        )

    def make_request(self, conversation, add_image=None, max_tokens=None):

        # Update conversation roles using your scheme
        conversation = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": content}
            for i, content in enumerate(conversation)
        ]

        # Chat templates
        USER_CHAT_TEMPLATE = "<start_of_turn>user\n{prompt}<end_of_turn>\n"
        MODEL_CHAT_TEMPLATE = "<start_of_turn>model\n{prompt}<end_of_turn>\n"

        # Create a formatted prompt from the updated conversation
        formatted_prompt = ""
        for turn in conversation:
            if turn["role"] == "user":
                formatted_prompt += USER_CHAT_TEMPLATE.format(prompt=turn["content"])
            else:
                formatted_prompt += MODEL_CHAT_TEMPLATE.format(prompt="model response.")

        # Adding a placeholder model turn to end the conversation
        formatted_prompt += "<start_of_turn>model\n"
        conversation = formatted_prompt

        assert self.model is not None, "Model is not loaded. Call load_model() first."

        out = self.model.generate(
            conversation, device=torch.device(self.machine_type)
        )  # output_len=60)
        return out


if __name__ == "__main__":
    # Example usage:
    gemma_instance = GemmaModel(variant="gemma:2b-it", machine_type="cuda")
    generated_sample = gemma_instance.generate_sample(
        "Write a poem about an llm writing a poem.", output_len=60
    )
    print(generated_sample)
