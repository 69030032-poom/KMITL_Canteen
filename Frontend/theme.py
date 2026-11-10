from pathlib import Path
import customtkinter as ctk
from PIL import Image

ORANGE = '#C94716'
ORANGE_HOVER = '#A93810'
CREAM = '#FFF8F0'
PEACH = '#FCE6D7'
TEXT = '#28231F'
MUTED = '#6F6258'
BORDER = '#E9DED3'


def add_canteen_art(parent, width=180, height=160):
    path = Path(__file__).resolve().parent.parent / 'assets' / 'canteen_background.png'
    if not path.exists():
        return None
    with Image.open(path) as source:
        picture = source.convert('RGB')
        picture = picture.crop((0, picture.height // 3, picture.width // 2, picture.height))
        art = ctk.CTkImage(light_image=picture, dark_image=picture, size=(width, height))
    label = ctk.CTkLabel(parent, text='', image=art)
    label.image = art
    return label
