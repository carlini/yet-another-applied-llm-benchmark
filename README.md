# Yet Another Applied LLM Benchmark

This is a benchmark I made, for me, to test how well language models perform
on tasks I care about. I know I care about them because each test is directly
derived from something I've asked a LLM to perform for me in the last year.

For example, there are tests in this benchmark that evaluate the ability of a model to:
- convert a python function to an equivalent-but-faster c function;
- decompile python bytecode to functional source code;
- explain the functionality of minified javascript;
- identify the encoding format (in this case, uuencoded) of some data;
- write a parser from a BNF-like grammar;
- convert some english sentences to SQL queries; or,
- write some bash oneliners

There are two defining features of this benchmark that make it interesting:

1. I've implemented a simple dataflow domain specific language to make it easy for
me (or anyone else!) to add new tests that realistically evaluate model capabilities.

2. Directly as a result of this, I've written nearly 100 tests for different
situations I've actually encountered when working with LLMs as assistants.

For example, here's a complete test to evaluate if a model can write a "hello world" program.

```python
'Write a "hello world" program in python' >> LLMRun() >> PythonRun() >> SubstringEvaluator("hello world")
```

I first ask the model to write hello world, then run that program (in a docker
container, seamlessly behind the scenes), and then check if stdout contains "hello world".
(You should read the `>>` operator as "and then do". So "a >> b" means "do a, and then do b".)

More interestingly, here's a test case that first asks a model to produce code that
draws a flag. To evaluate it, I run the code, partially judge it with another
language model, and then fully evaluate the output by comparing to a reference solution.

```python
"Write a C program that draws an american flag to stdout." >> LLMRun() >> CRun() >> \
    LLMRun("What flag is shown in this image?") >> \
        (SubstringEvaluator("United States") | SubstringEvaluator("USA") | SubstringEvaluator("America"))
```

This DSL makes it easy for me to evaluate significantly more diverse and
more sophisticated behavior than any other evaluation benchmark I'm aware of.
This is helpful for determining whether or not models are capable of performing tasks I actually care about.


## Results

I've evaluated a few models on this benchmark. Here's how they perform:
* GPT-4: 49% passed
* GPT-3.5: 30% passed
* Claude 2.1: 31% passed
* Claude Instant 1.2: 23% passed
* Mistral Medium: 25% passed
* Mistral Small 21% passed
* Gemini Pro: 21% passed

A complete evaluation grid is available [here](https://nicholas.carlini.com/writing/2024/evaluation_examples/index.html).


## What this is not

A serious academic benchmark.

In more words: this is not meant to try to rigorously evaluate the capabilities of
models on any particular task. It's not meant to be something you can use to decide
which model is more capable, more knowledgeable, more factual, less biased, less
harmful, more aligned, more helpful, or anything else.

The questions are not optimally prompt-engineered. It is entirely
possible---and indeed likely!---that a better phrasing of some of the questions
would allow the model to give a better answer.

But I am lazy.

I do not want to remind the model it is AN EXPERT IN PYTHON
and tell it that I'll give it a $100,000 tip for giving the right answer
OR I WILL MURDER A KITTEN but please pause....take a deep breath....and think step
by step by step before answering.
(Or whatever the current incantation is people use to get models to work best.)

I just want to type my question and get the right answer.
So this benchmark tests for that,
on types of questions I've actually cared about having answered.

### Failing a question doesn't mean much

As a result of my (often intentional) lack of prompt engineering,
when a model fails a question, you won't learn very much. Maybe my question was
just poorly worded. Maybe it was ambiguous in some way.

Instead, these tests are designed so that I learn something when the model passes.
You don't luck your way into correctly compiling Rust programs
without having some skill at the language. But you might luck your
way into failing by naming the function something I didn't expect and so your
correct code just is never invoked.


## What this is

Again, it's just a collection of questions I've actually asked language models to solve for me
to help with various programming tasks,
interspursed with a few questions I've asked language models just for fun.
The questions are, for the most part, unmodified questions as I typed them.
This means they may not be the most clearly worded
(e.g., `In python what __thing__ do I use for ~, kind of like how __add__ is for +`,
with the answser I'm expecting is `__inv__`).
Other questions are "unfair" because they require recent knowledge
(e.g., "what is the hidden dimension of llama-2 70b?").
But I care if a model can answer these correctly for me.


# Installing

Getting this benchmark up and running is fairly straightforward.

## Python requirements

On the python side you'll just need to run
`pip install -r requirements.txt` to install the python dependencies.

If you want to run it and evaluate a wide range of models you'll also need
`pip install -r requirements-extra.txt` to install the other models.


## Podman (preferred)

I want to run things in a container to keep them basically safe.
Docker is nicer and has slightly better security controls (and so you can
use that if you want below) but on linux you need to be root or give your
user almost-root permissions to start new docker jobs. This scares me a bit.

So I prefer to use podman. Install it however you're supposed to for your
system.


## Docker (optional)

Again this is fairly system dependent so you'll have to go somewhere else to find
out how to install it for your system.


## Why do I need docker/podman?

The test cases in this benchmark are evaluated by directly
executing code that comes out of a language model.
Some tests ask the model to rename files, move files around, or make other
state-changing operations to your machine.

While I don't think these models have it out for us and will emit `rm -rf /` out of
malice or spite, it's entirely possible (and even likely!) that they'll produce buggy
code that will just accidentally trash your computer.
So, to safeguard against this, all LLM output is evaluated from within a
temporary docker container that gets deleted immediately after the test is complete.

(There's also another reason, though: some of the tests assume a fresh install of
Ubuntu with particular dependencies in various places. These tests might behave
differently on your local machine than they do from within the docker VM.)

If you like to live dangerously (VERY MUCH NOT RECOMENDED) then there is
a flag in the code
`I_HAVE_BLIND_FAITH_IN_LLMS_AND_AM_OKAY_WITH_THEM_BRICKING_MY_MACHINE_OR_MAKING_THEM_HALT_AND_CATCH_FIRE`
that you can set to True and then this will just eval() everything that comes
out of the LLMs on your machine directly.


# Setup

Once you've installed everything,
there are a few setup steps before you can run the benchmark.

## Add API keys

You should add API keys for any model you want to evaluate. The keys are stored
in the config.json file. You can find a template at [config.json.example](config.json.example)

Whatever model you are testing, you will also need to load API keys for OpenAI as the default
evaluation model. This is because a few of the questions require evaluation by a second language model
to judge correctness.
These secondary evaluations are as simple as possible, but using a high-quality model
here is helpful to ensure consistency in the results.

I have had good success using gpt-4-turbo as the evaluation model, but you can configure
any model that you want as the evaluator. In my experiments, I had almost identical
results with the (cheaper) gpt-3.5-turbo, but in a few cases having the more capable
evaluation model gives more reliable results.

## Set up docker/podman container [highly recommended]

To start you'll need to create the docker container where the tests will run.
This will first require that you install docker on your machine.
Once you've done that, you can then build the image:

```bash
docker build -t llm-benchmark-image . # if you're using docker
podman build -t llm-benchmark-image . # if you're using podman
```

## Set up selenium/chrome

A few test cases require Selenium and Chrome to test if models can generate valid
html/javascript programs. Installing the requirements file should install selenium
for you, but you'll also need to make sure you install chrome. If you're on
ubuntu then you can just run

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```


# Running the benchmark

Once you've set up your environment, you can run the entire benchmark in just one line:

```bash
python main.py --model gpt-3.5-turbo --run-tests --generate-report
```

This command will run every single test that's configured on one model.
It will therefore take some time, and also will cost you a few dollars in
language model queries. After you can view the full reslt html file in the
directory `evaluation_examples`.

It will also save a cache of this run, so that the next time you can run
a new model and view the two results side-by-side.

If you want to run individual test cases, you can do that too in two ways.
One is to just directly run test

```bash
PYTHONPATH='.' python tests/print_hello.py
```
* Explore the `run_a_simple_testcase.ipynb` notebook to quickly run a sample test case on Colab. 

The other, if you want to save the result of this run so you can load it later,
is to run the main script and specify which test(s) you want to run.
(Be careful if you do this, though, beacuse it will overwrite any prior run.)


```bash
python main.py --test print_hello --run-tests --model gpt-3.5-turbo-0125
```


# Modifying the benchmark

## Adding your own LLM

This framework is fairly modular.
If you'd like to test a new LLM, you'll just need to add a new file to llms/[model_name]_model.py
which implements an inference function. From there, modify [llm.py](llm.py) to include the
appropriate model.

## Adding new test cases

As discussed above, I've built a small dataflow DSL to implement test cases.
This should let anyone add new test cases fairly easily.
Let me repeat the initial test case examples in full:

```python
TestHelloWorld = 'Print "hello world" in python' >> LLMRun() >> \
      ExtractCode() >> PythonRun() >> SubstringEvaluator("hello world")
```

Recall that you should read the `>>` operator as "and then do".
If you're a bash person, it's like a `|` pipe.
If you're a haskel person, it's like the `$` operator.
- We start by running the LLM we want to test with the prompt: Print "hello world" in python. 
- The model will probably give some code, but might also give an explanation or start by saying "Sure! I can answer your question." So we take whatever output came out of the model and pass it through a function to just extract the first code block.
- We then actually go and run this python code, whatever it is. To be somewhat safe we do this by spawning a new docker env and run the code there.
- And finally, we verify that the code was correct, and the output of the python contains a substring of "hello world".

This dataflow pipeline also lets you do more complex verification.
Below is the same example as from the top where I evaluate a model's
ability to understand how to draw .bmp images.


```python
TestFlagDraw = "Write a C program that draws an american flag to stdout as a bmp." >> \
       ExtractCode() >> CRun() >> LLMVisionRun("What flag is shown in this image?") >> \
          (SubstringEvaluator("United States") | \
           SubstringEvaluator("USA") | \
           SubstringEvaluator("America"))
```

Here, after asking the model to draw the flag and running the resulting C code,
I evaluate the model by asking *another* model what flag has been drawn,
and checking if it says something like the US flag.
Is this a perfect check? No.
But verification is usually easier than generation, and so it's probably a good
enough approximation of what I want.


# Contributing

If you'd like to add your own tests to this benchmark feel free to open a PR!
I'd be happy to accept basically anything interesting.

## Adding new tests

There are only a few requirements for adding a test.

1. Test cases must be mechanistically verifiable. This is very limiting, I know. A whole lot of
what I use LLMs for isn't verifiable in this way. Especially when I'm giving them large
blocks of code and asking for specific changes that are hard to unit test. But in order for
these to be useful your test must be easy to verify.

2. Test cases should complete quickly. I don't want to wait several minutes just for one test to run.

3. Tests should not be evaluated against LLMs during construction. Don't modify the test because
the model gave an answer you didn't like. Most LLMs are stochastic enough that there is *some*
way to elicit most behavior with enough trial and error. I want to see how the model answers
with a human-written test, as they are normally asked, before LM refinement.

4. Tests should be designed so that *passing* demonstrates some interesting model capability.
Making "gotcha" tests that are designed to show models fail in some way are not useful
in this setup.

3. Test cases must not download large amounts of data from the internet.
Someone else shouldn't have to pay for each run of this benchmark.
If you need to test a library add it to the Dockerfile.


## Fixing tests

Are there any tests here that are broken? I tried my best to make them all correct but can't
guarantee correctness for sure. If so I'd be happy to accept fixes.

But please note: a broken test means one where the answer is **objectively wrong**. Like a
test that says 6 is prime. A test that just expects a specific answer to an ambiguous question
is not wrong. For example, one test asks
"What do I do to fix AutoModel.from_pretrained to make it auto model with lm head"
and expects the model to tell me that I should be using the class "AutoModelForCausalLM";
even though the class "AutoModelWithLMHead" exists, that's not what I was looking for.

# I want to cite this in an academic paper

No you probably don't. At least, you probably don't if you're trying to compare
why your new model is better or something.
This is not meant to be something for academic papers and only evaluates
a very specific set of capabilities.
For all the reasons mentioned earlier I don't think this benchmark
will accurately capture what academic people should care about for their models.
Good for "useful for me?": yes. Good for "is my model better?": I don't think so.
But I've now had at least a few people ask me about this who appear unswayed by the
above argument.

So here's my answer: if you want to user this in a paper,
then link to this github project AND INCLUDE THE GIT COMMIT HASH YOU USED.
I make NO GUARANTEES that I won't just arbitrarily edit test cases without
warning. In fact, it's already happened in #1! And #3! And #6.
So if you want your paper
to be at all scientific make sure to include the git commit hash.


# License

Copyright (C) 2024, Nicholas Carlini <nicholas@carlini.com>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
