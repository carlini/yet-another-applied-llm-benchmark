from evaluator import *

DESCRIPTION = "Test if the model can make a PNG get detected as an ELF executable."

TAGS = ["coding"]

question = """
I have a file called `image.png`. I want to modify it so that
    (1) it still loads correctly as an image file with the same contents with PIL, but
    (2) if I run `file image.png`, it should say that it is an ELF executable.

Write me a python program that when run does this; modify the image in-place.
"""


def test_ok():
    import os
    if 'ELF' not in os.popen("file image.png").read():
        return False
    from PIL import Image
    img = Image.open("image.png").numpy()
    
    return img[0, 0].tolist() == [255, 0, 0] and img[0, 1].tolist() == [0, 255, 0] and img[0, 2].tolist() == [0, 0, 255] and img.shape == (100, 100, 3)


def setup_image():
    from PIL import Image
    import numpy as np
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[0, 0] = [255, 0, 0]
    img[0, 1] = [0, 255, 0]
    img[0, 2] = [0, 0, 255]
    Image.fromarray(img).save("image.png")


TestMakePNGToELF = Setup(setup_image) >> question >> LLMRun(question) >> ExtractCode() >> PythonRun() >> PyEvaluator(test_ok)

if __name__ == "__main__":
    print(run_test(TestMakePNGToELF))
