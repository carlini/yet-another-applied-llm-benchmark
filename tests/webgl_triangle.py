from evaluator import *

DESCRIPTION = "Test if the model can generate an HTML file with WebGL code that draws an image."

TAGS = ['code', 'visual', 'html']

question = """
Draw an image of a triangle using WebGL in a single HTML file. Make the canvas take the full page.
"""

TestDrawTriangle = question >> LLMRun() >> ExtractCode(keep_main=True, lang="html/javascript") >> (~SubstringEvaluator("THREE.") & (SeleniumDraw() >> LLMVisionRun("This is a screenshot of a webpage that draws something with webgl. I'm trying to see if it drew what I wanted. Describe what is drawn in this image?") >> LLMRun("Does this answer say that there is a picture of a triangle \"<A>\"? Answer \"Yes it does\" or \"No it does not\".", llm=EVAL_LLM) >> SubstringEvaluator("es it does")))

question2 = """
Draw an image of a house with a chimney using WebGL in a single HTML file. Make the canvas take the full page.
"""

TestDrawHouse = question2 >> LLMRun() >> ExtractCode(keep_main=True, lang="html/javascript") >> (~SubstringEvaluator("THREE.") & (SeleniumDraw() >> LLMVisionRun("This is a screenshot of a webpage that draws something with webgl. I'm trying to see if it drew what I wanted. Describe what is drawn in this image?") >> LLMRun("Does this answer say that there is a picture of a house with a chimney \"<A>\"? Answer \"Yes it does\" or \"No it does not\".", llm=EVAL_LLM) >> SubstringEvaluator("es it does")))

if __name__ == "__main__":
    print(run_test(TestDrawHouse))
