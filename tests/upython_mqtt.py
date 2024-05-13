from evaluator import *

DESCRIPTION = "Test if a model can write upython code with an obscure module."

TAGS = ['python', 'code']

question = """
Write a python program that I can use to run on my raspberry pi pico w zero that will check for mqtt messages. Don't block, and blink the LED on every loop iteration so I know it's polling. When it gets a message then set the LED solid for a second.
"""

# crude testing because there isn't an actual pico w to run this on...
TestUPythonMQTT = question >> LLMRun() >> (SubstringEvaluator("check_msg") & SubstringEvaluator("MQTTClient") & SubstringEvaluator("set_callback") & SubstringEvaluator('WLAN') & SubstringEvaluator("STA_IF"))

if __name__ == "__main__":
    print(run_test(TestUPythonMQTT))

