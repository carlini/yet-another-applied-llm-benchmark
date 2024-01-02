from evaluator import *

question = """
Draw an image of a house with a chimney using WebGL in a single HTML file. Make the canvas take the full page.
"""

DrawTriangleTest = question >> LLMRun() >> ExtractCode(keep_main=False) >> SeleniumDraw() >> LLMVisionRun("What object is drawn in this image?") >> LLMRun("Does this answer say that there is a picture of a house with a chimney \"<A>\"? Answer \"Yes it does\" or \"No it does not\".", llm=EVAL_LLM) >> SubstringEvaluator("es it does")

if __name__ == "__main__":
    print(run_test(DrawTriangleTest))
