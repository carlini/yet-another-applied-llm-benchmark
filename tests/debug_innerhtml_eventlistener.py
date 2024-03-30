from evaluator import *

DESCRIPTION = "Test if a model knows that editing the innerHTML clears event listeners."

TAGS = ['explain']

question = """
Why doesn't the slider onchange event fire when I run this code?

```
<body>

<script>

var candidate_paper_list;

class Dropdown {
    constructor(parent_html, parent_node) {
        var r = Math.random()
        parent_html.innerHTML += `<div class="autocomplete-container" style="border: 1px solid #000; padding: 1em">
        <label for="search-input">Search Paper Titles:</label>
        <input type="text" id="search-input-${r}" autocomplete="off">
        <div id="autocomplete-results"></div>
</div>`;

    }

}

class Mul {
    constructor(parent_html, parent_node) {
        var div = document.createElement("div");
        div.style = "border: 1px solid #000; padding: 1em"
        parent_html.appendChild(div);
        var slider = document.createElement("input");
        slider.type = "range"
        slider.id = "foo"
        slider.min = "0"
        slider.max = "100"
        slider.step = ".1"
        this.slider = slider
        div.appendChild(slider);
        this.node = div;
        div.appendChild(document.createElement("br"));
        parent_node.child = this;

        slider.addEventListener("input", (event) => {
            console.log(event.target.value);
        });

    }

    serialize() {
        console.log("VALUE", this.slider.value);
        console.log("VALUE", this.slider);
        let positive_papers = ['const_mul', this.child.serialize(), +this.slider.value];
        return positive_papers;
    }
}


document.body.onload = function() {
    var mul = new Mul(document.body, {})
    root_node = mul;
    var dropdown = new Dropdown(mul.node, mul);
}

</script>
</body>
```

Tell me how to fix it.
"""

evaluation = """
Below is a student's answer to a question about what a particular instruction does: <A>

Does the student's say something similar to "editing the innerHTML clears event listeners"?

If the answer is correct say "The student passes" otherwise "The student fails".
"""

TestInnerHTMLEventListener = question >> LLMRun() >> LLMRun(evaluation, llm=EVAL_LLM) >> SubstringEvaluator("student passes")
    

if __name__ == "__main__":
    print(run_test(TestInnerHTMLEventListener))
