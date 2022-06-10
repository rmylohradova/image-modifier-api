from pydantic import BaseModel, validator, Field
from enum import Enum
from typing import Optional


class Band(str, Enum):
    rgb = 'rgb'
    l = 'l'


class MergedBand(str, Enum):
    description = 'pink/green/blue'
    pink = 'pink'
    blue = 'blue'
    green = 'green'


class TextPlacement(str, Enum):
    all = 'center/top_center/bottom_center/center_left/center_right'
    center = 'center'
    top_center = 'top_center'
    bottom_center = 'bottom_center'
    center_left = 'center_left'
    center_right = 'center_right'


class TextFont(str, Enum):
    all = 'arial/bold/cursive/motion_picture/southern_aire'
    arial = 'arial'
    bold = 'bold'
    cursive = 'cursive'
    motion_picture = 'motion_picture'
    southern_aire = 'southern_aire'


class ModifyBy(BaseModel):
    height: int | None = None
    width: int | None = None
    rotate: int | None = None
    brightness: int | None = None
    color: int | None = None
    sharpness: int | None = None
    contrast: int | None = None
    left_right: bool = False
    top_bottom: bool = False
    band: Band
    blur: bool = False
    minfilter: bool = False
    maxfilter: bool = False
    sharpen: bool = False
    contour: bool = False
    smooth: bool = False
    detail: bool = False
    emboss: bool = False
    find_edges: bool = False
    edge_enhance: bool = False
    merge_colors: MergedBand
    on_text: str | None = None
    text_color: str | None = None
    text_placement: TextPlacement
    text_size: int | None = None
    font: TextFont

    @validator('*', pre=True)
    def blank_string(cls, value):
        if value == "":
            return None
        return value

    @validator('height', 'width')
    def check_size(cls, value):
        if value:
            if value < 1 or value > 1080:
                raise ValueError('must be within 1-1080 range')
        return value

    @validator('rotate')
    def check_degrees(cls, value):
        if value:
            if value < 1 or value > 360:
                raise ValueError('must be from 1 to 360 degrees')
        return value

    @validator('brightness', 'color', 'sharpness', 'contrast', 'text_size')
    def check_range(cls, value):
        if value:
            if value < 1 or value > 1000:
                raise ValueError('must be from 1 to 1000')
        return value


