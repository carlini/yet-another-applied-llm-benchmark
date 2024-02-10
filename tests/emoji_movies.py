from evaluator import *

DESCRIPTION = "A for-fun test to see if the model can go movie title -> emoji -> movie title."

TAGS = ['fun']

question = """
For each of the following ten movies give at most 5 emoji that would best describe the movie.

Give your answer as a JSON array. So If I asked for
```["Finding Nemo", "Toy Story"]```

you might might answer

```json
{"Finding Nemo": ["🐠", "🐟", "🐡", "🐬", "🐳"],
"Toy Story": ["🚀", "⚔️,", "🤖", "👽", "🌌"]}
```.

Each emoji must be a single utf8 character. ABSOLUTELY NO ZERO WIDTH JOINING. (So, max(len(emoji) for movie in result.values() for emoji in movie) == 1)

Now give me answers for these movies:

```["The Lion King", "The Nightmare Before Christmas", "The Godfather", "The Matrix", "Casablanca", "Raiders of the Lost Ark", "V for Vendetta", "The Princess Bride", "Back to the Future", "Dune"]```

Give ONLY a JSON output. Nothing else.
"""

undo = """
For each of the following ten movies described by 5 emoji, give the movie title that best matches.

Give your answer as a JSON list. So If I asked for
```[["🐠", "🐟", "🐡", "🐬", "🐳"], ["🚀", "⚔️,", "🤖", "👽", "🌌"]]```

You might answer

```json
["Finding Nemo", "Toy Story"]]
```.

Now give me answers for these movies:

```<A>```

What are the names of the movie titles?
"""

def extract(x):
    try:
        x = json.loads(x)
    except:
        print("Failed processing")
        return ""
    send = list(x.values())
    # I'll be nice...
    send = [[x for x in y if len(x) <= 2] for y in send]
    return str(send).replace("], [", "],\n[")

def count(x):
    try:
        x = json.loads(x)
        count = 0
        for correct, guessed in zip(["The Lion King", "The Nightmare Before Christmas", "The Godfather", "The Matrix", "Casablanca", "Raiders of the Lost Ark", "V for Vendetta", "The Princess Bride", "Back to the Future", "Dune"], x):
            if correct.lower() == guessed.lower():
                count += 1
        return count >= 8, "OK"
    except:
        return False, "Not a JSON list"


TestEmojiMovie = question >> LLMRun() >> ExtractJSON() >> PyFunc(extract) >> LLMRun(undo) >> ExtractJSON() >> PyFunc(count)

if __name__ == "__main__":
    print(run_test(TestEmojiMovie))
