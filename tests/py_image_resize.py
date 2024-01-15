from evaluator import *

DESCRIPTION = "Test if the model can resize several images in a given subdirectory."

TAGS = ['code', 'python']

question = """Write function resize_image in python that open get a folder path as in put and looks for all of the images files in that folder using only pillow and resize them to 32x32 and overwrite it. Just give me the python code that I can run by python code.py and the default folder is /tmp """




def setup():
    from PIL import Image
    import random
    import os
    def create_random_image(file_path):
        # Random size between 100x100 and 800x800
        width, height = random.randint(100, 800), random.randint(100, 800)
        # Random color
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Create an image with the random color
        image = Image.new("RGB", (width, height), color)
        # Save the image
        image.save(file_path)
    for i in range(10):
        file_path = os.path.join('/tmp/', f"random_image_{i+1}.jpg" if random.random() > 0.5 else  f"random_image_{i+1}.jpeg"  , )
        create_random_image(file_path)

def test():
    import os
    from PIL import Image
    # Iterate over each file in the folder
    target_size = (32,32)
    folder_path = '/tmp/'
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        # Check if the file is an image
        if file_path.lower().endswith(('.jpg', '.jpeg')):
            # Open the image
            with Image.open(file_path) as img:
                # Check if the image size matches the target size
                if img.size != target_size:
                    print('size is ',img.size)
                    return False
    return True


TestImgResize = Setup(setup) >> question >> LLMRun() >> ExtractCode(keep_main=True) >> Echo() >> PythonRun() >> PyEvaluator(test)

if __name__ == "__main__":
    print(run_test(TestImgResize))


