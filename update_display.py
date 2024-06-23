from inky.auto import auto
from PIL import Image
import json
display = auto()


# get first not shown image from status.json
def get_next_image():
    with open('photos.json', 'r') as f:
        status = json.load(f)
    for image in status:
        if not image['shown']:
            image['shown'] = True
            with open('photos.json', 'w') as f:
                json.dump(status, f)
            return image['image']
        
    # switch all images to not shown
    for image in status:
        image['shown'] = False

    with open('photos.json', 'w') as f:
        json.dump(status, f)

    return get_next_image()

# show image on display
img = Image.open(f'photos/{get_next_image()}')
display.set_image(img)
display.show()