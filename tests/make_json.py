from evaluator import *

DESCRIPTION = "Test if the model can successfully convert unstructured data to JSON."

TAGS = ['data']

question = """
Create a JSON metadata for these models:

Mistral-7B-v0.1
RedPajama-INCITE-7B-Base
RedPajama-INCITE-Base-3B-v1
falcon40b
falcon7b
gpt2-xl
llama-65b
llama-7b
neo-1.3
neo-2.7
neo-6
open_llama_3b_v2
open_llama_7b_v2
opt-1.3b
opt-6.7b
pythia-1.4
pythia-1.4-dedup
pythia-6.9
pythia-6.9-dedup

With the format:

{"Mistral-7B-v0.1": {"size": 7, dataset: "", "family": "Mistral"}, ...}

where family is one of 

    base = [
        'pythia',
        'llama',
        'Mistral',
        'gpt2',
        'opt',
        'RedPajama',
        'neo',
        'open_llama',
        'falcon'
    ]

gpt2-xl is 1.5b parameters.

"""


TestMakeJson = question >> LLMRun() >> ExtractJSON() >> JSONSubsetEvaluator({
  "Mistral-7B-v0.1": {"size": 7, "dataset": "", "family": "Mistral"},
  "RedPajama-INCITE-7B-Base": {"size": 7, "dataset": "", "family": "RedPajama"},
  "RedPajama-INCITE-Base-3B-v1": {"size": 3, "dataset": "", "family": "RedPajama"},
  "falcon40b": {"size": 40, "dataset": "", "family": "falcon"},
  "falcon7b": {"size": 7, "dataset": "", "family": "falcon"},
  "gpt2-xl": {"size": 1.5, "dataset": "", "family": "gpt2"},
  "llama-65b": {"size": 65, "dataset": "", "family": "llama"},
  "llama-7b": {"size": 7, "dataset": "", "family": "llama"},
  "neo-1.3": {"size": 1.3, "dataset": "", "family": "neo"},
  "neo-2.7": {"size": 2.7, "dataset": "", "family": "neo"},
  "neo-6": {"size": 6, "dataset": "", "family": "neo"},
  "open_llama_3b_v2": {"size": 3, "dataset": "", "family": "open_llama"},
  "open_llama_7b_v2": {"size": 7, "dataset": "", "family": "open_llama"},
  "opt-1.3b": {"size": 1.3, "dataset": "", "family": "opt"},
  "opt-6.7b": {"size": 6.7, "dataset": "", "family": "opt"},
  "pythia-1.4": {"size": 1.4, "dataset": "", "family": "pythia"},
  "pythia-1.4-dedup": {"size": 1.4, "dataset": "", "family": "pythia"},
  "pythia-6.9": {"size": 6.9, "dataset": "", "family": "pythia"},
  "pythia-6.9-dedup": {"size": 6.9, "dataset": "", "family": "pythia"}
})

if __name__ == "__main__":
    print(run_test(TestMakeJson))
