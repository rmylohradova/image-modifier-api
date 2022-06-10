from fastapi import UploadFile
from modifier import schemas
import os

from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
from string import ascii_letters
import textwrap
import time


def is_image(filename: str) -> bool:
    valid_extensions = ('.jpeg', '.jpg', 'png')
    return filename.endswith(valid_extensions)


def upload_image(directory: str, file: UploadFile):
    if is_image(file.filename):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        image_name = timestr + file.filename.replace(" ", "-")
        with open(f"{directory}/{image_name}", "wb+") as image_file_upload:
            image_file_upload.write(file.file.read())
            image_path = directory + image_name
            return image_path
    return None


def convert(percent):
    final = (percent/100)+1
    return final


def apply_font(font):
    font_file = 'modifier/files/fonts/arial.ttf'
    if font == "arial":
        font_file = 'modifier/files/fonts/arial.ttf'
    elif font == "cursive":
        font_file = 'modifier/files/fonts/cursive.ttf'
    elif font == 'bold':
        font_file = 'modifier/files/fonts/COOPBL.ttf'
    elif font == "motion_picture":
        font_file = 'files/fonts/MotionPicture.ttf'
    elif font == "southern_aire":
        font_file = 'modifier/files/fonts/SouthernAire.ttf'
    return font_file


def multi_text_center(txt, txt_color, img, txt_size, font):
    dctx = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(apply_font(font), txt_size)
    avg_char_width = sum(fnt.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
    max_char_count = int(img.width/ avg_char_width)
    text = textwrap.fill(text=txt, width=max_char_count)
    dctx.text(
        (img.width / 2, img.height/2),
        text,
        font=fnt,
        fill=txt_color,
        anchor='mm',
        align='center'
    )


def one_line_text(txt, txt_color, img, txt_size, font, place):
    dctx = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(apply_font(font), txt_size)
    if place == 'top_center':
        dctx.text(
            (img.width / 2, 0 + 10),
            txt,
            font=fnt,
            fill=txt_color,
            anchor='ma',
        )
    if place == 'bottom_center':
        dctx.text(
            (img.width / 2, img.height - 10),
            txt,
            font=fnt,
            fill=txt_color,
            anchor='mb',
        )
    if place == 'center_left':
        dctx.text(
            (0+10, img.height / 2),
            txt,
            font=fnt,
            fill=txt_color,
            anchor='ls',
        )
    if place == 'center_right':
        dctx.text(
            (img.width-10, img.height / 2),
            txt,
            font=fnt,
            fill="white",
            anchor='rs',
        )


def maybe_resize(width, height, image: Image):
    if width and height:
        box = (width, height)
        sized = image.resize(box)
        return sized
    # elif width is None and height is None:
    elif width == 0 and height == 0:
        return image


def maybe_rotate(degree, image: Image):
    if degree:
        rotated = image.rotate(degree)
        return rotated
    # elif degree is None:x
    elif degree == 0:
        return image


def maybe_brighten(value, image: Image):
    if value:
        img_bright = ImageEnhance.Brightness(image)
        bright_value = value/100+1
        brightened = img_bright.enhance(bright_value)
        return brightened
    # if value is None:
    elif value == 0:
        return image


def maybe_enhance_color(value, image: Image):
    if value:
        img_color = ImageEnhance.Color(image)
        color_value = value/100+1
        color_enhanced = img_color.enhance(color_value)
        return color_enhanced
    # elif value is None:
    elif value == 0:
        return image


def maybe_sharpen(value, image: Image):
    if value:
        img_sharp = ImageEnhance.Sharpness(image)
        sharp_value = value/100+1
        sharpened = img_sharp.enhance(sharp_value)
        return sharpened
    elif value == 0:
    # elif value is None:
        return image


def maybe_enhance_contrast(value, image: Image):
    if value:
        img_contrast = ImageEnhance.Contrast(image)
        contrast_value = value/100+1
        contrasted = img_contrast.enhance(contrast_value)
        return contrasted
    # elif value is None:
    elif value == 0:
        return image


def maybe_filter(image: Image, blur, minfilter, maxfilter, sharpen, contour, smooth, detail, emboss, edge_enhance, find_edges):
    if blur:
        image = image.filter(ImageFilter.BLUR)
    if minfilter:
        image = image.filter(ImageFilter.MinFilter)
    if maxfilter:
        image = image.filter(ImageFilter.MaxFilter)
    if sharpen:
        image = image.filter(ImageFilter.SHARPEN)
    if contour:
        image = image.filter(ImageFilter.CONTOUR)
    if smooth:
        image = image.filter(ImageFilter.SMOOTH)
    if detail:
        image = image.filter(ImageFilter.DETAIL)
    if emboss:
        image = image.filter(ImageFilter.EMBOSS)
    if edge_enhance:
        image = image.filter(ImageFilter.EDGE_ENHANCE)
    if find_edges:
        image = image.filter(ImageFilter.FIND_EDGES)
    return image


def maybe_change_color(color, image):
    if color:
        r, g, b = image.split()
    if color == 'pink':
        image = Image.merge("RGB", (r, b, g))
    if color == 'blue':
        image = Image.merge("RGB", (b, g, r))
    if color == 'green':
        image = Image.merge("RGB", (g, r, b))
    return image

def process(params, im: Image):
    im = maybe_resize(params.width, params.height, im)
    im = maybe_rotate(params.rotate, im)
    im = maybe_brighten(params.brightness, im)
    im = maybe_enhance_color(params.color, im)
    im = maybe_sharpen(params.sharpness, im)
    im = maybe_enhance_contrast(params.contrast, im)
    if params.left_right:
        im = im.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
    if params.top_bottom:
        im = im.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    if params.band == 'rgb':
        im = im.convert('RGB')
    if params.band == 'l':
        im = im.convert('L')
    if params.blur:
        im = im.filter(ImageFilter.BLUR)
    im = maybe_filter(im, params.blur, params.minfilter, params.maxfilter,
                      params.sharpen, params.contour, params.smooth, params.detail,
                      params.emboss, params.edge_enhance, params.find_edges)
    im = maybe_change_color(params.merge_colors, im)
    if params.on_text:
        txt = params.on_text
        if params.text_placement == 'center':
            multi_text_center(txt, params.text_color, im, params.text_size, params.font)
        else:
            one_line_text(txt, params.text_color, im, params.text_size, params.font, params.text_placement)
    return im


# def modify_and_save(filter: schemas.Base, im_name):
#     with Image.open(f"files/original/{im_name}") as im:
#         save_path = os.path.join("./files/modified/", im_name)
#         modified_image = maybe_rotate(filter, im)
#         modified_image.save(save_path)
#         return save_path


