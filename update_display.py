from inky.auto import auto
from PIL import Image
import json
import os
display = auto()
dirname = os.path.dirname(__file__)
photos_json = os.path.join(dirname, 'photos.json')

# get first not shown image from status.json
def get_next_image():
    with open(photos_json, 'r') as f:
        status = json.load(f)

    if len(status) <= 1:
        return None
    
    for image in status:
        if not image['shown']:
            image['shown'] = True
            with open(photos_json, 'w') as f:
                json.dump(status, f)
            return image['image']
        
    # switch all images to not shown
    for image in status:
        image['shown'] = False

    with open(photos_json, 'w') as f:
        json.dump(status, f)

    return get_next_image()

# show image on display
f = get_next_image()
if f != None:
    img = Image.open(os.path.join(dirname, f'photos/{f}'))
    display.set_image(img)
    display.show()