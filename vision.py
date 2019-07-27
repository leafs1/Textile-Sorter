import os, io
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'Service_Account_Token.json'

client = vision.ImageAnnotatorClient()

global num 
num = 1
global condition
condition = "usable"
def localize_objects(path):
    global num
    global condition

    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations


    for object_ in objects:

        if object_.score >= 0.965:
            condition = "acceptable to sell"
        elif object_.score < 0.965:
            condition = "unacceptable to sell"
        else:
            pass

        print('\nObject#', num, 'is a {} and is {} (confidence: {}%).'.format(object_.name, condition, round(object_.score,3) * 100))
        num += 1

        
    obj_info = [object_.name, object_.score]

    return obj_info

object1 = localize_objects("goodtshirt.jpg")
object2 = localize_objects("slightly_torn_shirt.jpg")
