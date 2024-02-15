from evaluator import *

DESCRIPTION = "Test if the model can generate an HTML file using flexbox"

TAGS = ['code', 'html']

question = """
Generate an HTML file that uses flexbox to create a webpage with a header 200px at the top (colored red), and the rest of the body split 100px for a left sidebar (in blue), 100px for a right sidebar (in green), and the rest of the page in the middle (in white).
"""

def check(x):
    import io
    from PIL import Image
    import numpy as np
    img = Image.open(io.BytesIO(x))

    np_img = np.array(img)[:,:,:3]
    while np.mean(np_img[0]) >= 254:
        np_img = np_img[1:]
    while np.mean(np_img[:, 0]) >= 254:
        np_img = np_img[:, 1:]

    if np_img[0:200].std((0,1)).mean() > 20:
        return False

    if np_img[400:, :100].std((0,1)).mean() > 20:
        return False

    if np_img[400:, -100:-30].std((0,1)).mean() > 20:
        return False

    if np_img[0:200].mean((0,1)).argmax() != 0:
        return False

    if np_img[400:, :100].mean((0,1)).argmax() != 2:
        return False

    if np_img[400:, -100:].mean((0,1)).argmax() != 1:
        return False
    
    
    if np_img[:800, :100].std((0,1)).mean() < 20:
        return False

    if np_img[:800, -100:].std((0,1)).mean() < 20:
        return False
    
    return True

    

TestFlexbox = question >> LLMRun() >> ExtractCode(keep_main=True, lang="html/javascript") >> SeleniumDraw() >> PyFunc(check)

if __name__ == "__main__":
    print(run_test(TestFlexbox))

