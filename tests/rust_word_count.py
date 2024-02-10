from evaluator import *

DESCRIPTION = "Test if the model can write a rust program that performs word counting."

TAGS = ['code', 'rust']

question = """
Write a self-contained Rust program that prints a JSON output of how often each word appears in a text file located in /tmp/file.txt. So if the file contains "This is is is, an example" then the program should print to stdout. 

{"This": 1, "is": 2, "is,": 1, "an": 1, "example": 1}

Don't import any crates that would require a Cargo.toml file. I'll just compile it with `rustc yourfile.rs` and it should work. The program should be run by calling /path/to/rust_word_count with no arguments
"""

extra = "\nDo not import serde_json, write json output from scratch."

def setup():
    txt = "it was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way"
    open("/tmp/file.txt", "w").write(txt)


answer = {'the': 11, 'it': 10, 'was': 10, 'of': 10, 'we': 4, 'times,': 2, 'age': 2, 'epoch': 2, 'season': 2, 'had': 2, 'before': 2, 'us,': 2, 'were': 2, 'all': 2, 'going': 2, 'direct': 2, 'best': 1, 'worst': 1, 'wisdom,': 1, 'foolishness,': 1, 'belief,': 1, 'incredulity,': 1, 'Light,': 1, 'Darkness,': 1, 'spring': 1, 'hope,': 1, 'winter': 1, 'despair,': 1, 'everything': 1, 'nothing': 1, 'to': 1, 'Heaven,': 1, 'other': 1, 'way': 1}

TestRustCount = Setup(setup) >> StringNode(question) >> LLMRun() >> ExtractCode(keep_main=True) >> RustRun() >> ExtractJSON() >> JSONSubsetEvaluator(answer)

TestRustCountNoLib = Setup(setup) >> StringNode(question+extra) >> LLMRun() >> ExtractCode(keep_main=True) >> RustRun() >> ExtractJSON() >> JSONSubsetEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestRustCountNoLib))
