from evaluator import *

DESCRIPTION = "This test case tests if the model can convert a Game of Life pattern represented in RLE format to a numpy array."

TAGS = ['code', 'python']

question = """
Convert this game of life pattern

26$13b2o$14bo$14bobo$15b2o14$31b2o$30b2o$32bo13$46b2o$45b2o$47bo13$61b
2o$60b2o$62bo4$52b2o$52b2o$71bo$66b2ob3o$66bobobo$68bo$67b2o3$76b2o$
60b3o12b2o10bobo$52b3o7bo14bo8bo2bo4bo$51bo3bo5bo10b2o11b2o5b2o$50bo5b
o15bobo8b2o3bo8b2o$51bo3bo11b2o6bo9b2o10b2o$52b3o8b2obo2bo2bo2bo10bo2b
o$52bo2bo7b2o2b2o6bo11bobo$53b3o16bobo$53b2obo15b2o$54bobo$55bo3$52b2o
3b2o$52bobobobo$53b5o$54b3o$55bo7$54b2o$54b2o!


to a numpy array. Call the function `rle_to_arr(string, h, w)`
which should return a numpy array with .shape (h,w).
Fill the array with 1s, and empty with 0.
"""

rle = """
16b2o3b2o$2o$2o$19b2o$17b5o$21bo$17b3o$o16bo$o17b2o$bo16b2o$b2o$3bo$o
17b2o3b2o$2b2o14bobobobo$11bobo5b5o$11b2o7b3o$2o10bo8bo$b2o$b2o2$2o$bo
2$6bobo$2o3bo$bo3bo$o4bo2bo7bo$5b3o7b2o7bo$15bobo5b3o$22b5o$21b2o3b2o$
22b5o$22b5o$14b2o6bo2bo$14bobo4bo3bo$11b2obobo4bo$11bobobo5bob2o$13bo
8bo$4bobo6b2o$7bo5b3o50bo$7bo5b3o3b2o3b2o40b4o$4bo2bo5b3o3bo5bo41b4o$
5b3o5b2o35bo16bo2bo$13bo6bo3bo24bobo15b4o4b2o$11bobobo5b3o15b2o7bob2o
14b4o5b2o$11b2obobo21bobo6b2ob2o14bo8b2o$14bobo20bo6b3obob2o$14b2o12b
2o7bo2bo2bo2bo2bobo$28b2o7bo6b2o4bo16bobo$38bobo26b2o$39b2o27bo4b2o$
21b2o49bo2bo$21b2o28bobo18b3o$52b2o21b2o$52bo21bo$74b2o$59bo$62bo$59bo
14bo$62bo$61bob3o8bo$59b4o2bo9b2o$64bo$52bo$51b2o$40b2o8b2o4b2o5bo$40b
2o7b3o4b2o3bobo$50b2o4b2o2bobo11b2o$4bobo44b2o6bo2bo11b2o$7bo44bo7bobo
$o6bo53bobo$o3bo2bo55bo$5b3o5$4b4o$3bo3bo$7bo$3bo2bo3$o2b3o2b2o$2b5o2b
o64b3o$9o67bo$9b3o63bo$o7bo2bo$9b2o3$4b2o$o3b3o$o5b2obo5b2o$bo4bo2bo5b
2o$2o4b2obo$o3b3o$4b2o2$59b3o12b2o$61bo12b2o!
"""



test_case, answer = make_python_test([(f"(np.array(rle_to_arr('''{rle}''', 101, 77),dtype=np.uint32).flatten() * np.arange(77*101)).sum()", "1563304")])

TestRLEDecode = question >> LLMRun() >> ExtractCode() >> PythonRun(test_case) >> SubstringEvaluator(answer)

if __name__ == "__main__":
    print(run_test(TestRLEDecode))
