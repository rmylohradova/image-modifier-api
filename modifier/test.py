from PIL import Image
from image_services import process_image, maybe_resize, maybe_rotate, maybe_brighten,\
    maybe_enhance_color, maybe_sharpen, maybe_enhance_contrast
import os

from schemas import SmallChange


def save_modified_im(path, filters_ex):
    with Image.open(path) as im:
        im = process(filters_ex, im)
        save_path = os.path.join("files/modified/", path.split('/')[-1])
        im.show()
        im.save(save_path)


def process(params, im: Image):
    im = maybe_resize(params.width, params.height, im)
    im = maybe_rotate(params.rotate, im)
    im = maybe_brighten(params.brightness, im)
    im = maybe_enhance_color(params.color, im)
    im = maybe_sharpen(params.sharpness, im)
    im = maybe_enhance_contrast(params.contrast, im)
    return im


filters = SmallChange(
    height=100,
    width=500,
)
print(filters)
save_modified_im("files/original/20220608-125224babyyoda.jpeg", filters)
