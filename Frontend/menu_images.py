from functools import lru_cache
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageOps

# Names follow the photo order: left to right, then top to bottom.
PHOTO_SHEETS = {
    'menu_photo_sheet.png': [
        'ก๋วยเตี๋ยวหมูต้มยำ', 'ก๋วยเตี๋ยวเย็นตาโฟ', 'ข้าวมันไก่ต้ม',
        'ข้าวขาหมู', 'ข้าวผัด', 'ชานม',
    ],
    'menu_rice.png': [
        'กุนเชียง', 'หมูยอ', 'ข้าวกะเพรา',
        'ข้าวมันไก่ทอด', 'ข้าวมันไก่ย่าง', 'ข้าวสวย',
        'ข้าวหมูกรอบ', 'ข้าวหมูแดง', 'ข้าวเหนียว',
        'ข้าวไก่แดง', 'ไข่ดาว', 'ไข่เจียว',
    ],
    'menu_noodles.png': [
        'ก๋วยเตี๋ยวหมูน้ำข้น', 'ก๋วยเตี๋ยวหมูน้ำใส', 'ขนมจีนน้ำยากะทิ',
        'ขนมจีนป่าไก่โคราช', 'ขนมจีนเปล่า', 'บะหมี่–เกี๊ยว หมูแดง',
        'บะหมี่–เกี๊ยว ไก่แซ่บ', 'ผัดซีอิ๊ว', 'มาม่าผัดขี้เมา',
        'ราดหน้า', 'สุกี้น้ำ', 'สุกี้แห้ง',
    ],
    'menu_drinks.png': [
        'คาปูชิโน', 'ชาเขียว', 'ช็อกโกแลตลาเต้',
        'นมสดโอริโอ้', 'ลาเต้', 'ลาเต้เย็น',
        'อเมริกาโน่เย็น', 'เอสเพรสโซ่', 'โกโก้',
        'ชาไทย', 'ข้าวราดแกง', None,
    ],
    'menu_salads.png': [
        'ตำถั่ว', 'ตำแตง', 'ต้มยำทะเล',
        'ต้มยำหมูชิ้น', 'ต้มยำไก่', 'ยำอกไก่',
        'ลาบหมู', 'ลาบไก่', 'ส้มตำปูปลาร้า',
        'ส้มตำไทย', None, None,
    ],
}

MENU_PHOTOS = {}
for filename, names in PHOTO_SHEETS.items():
    for index, name in enumerate(names):
        if name is not None:
            MENU_PHOTOS[name] = (filename, index, len(names) // 3)


@lru_cache(maxsize=100)
def load_menu_picture(name, size):
    photo = MENU_PHOTOS.get(name)
    if photo is None:
        return None
    filename, index, rows = photo
    path = Path(__file__).resolve().parent.parent / 'assets' / filename
    if not path.exists():
        return None
    with Image.open(path) as sheet:
        width, height = sheet.width // 3, sheet.height // rows
        x, y = (index % 3) * width, (index // 3) * height
        picture = sheet.crop((x, y, x + width, y + height)).convert('RGB')
        return ImageOps.fit(picture, size, method=Image.Resampling.LANCZOS)


def get_menu_image(name, size=(240, 135)):
    picture = load_menu_picture(name, size)
    if picture is None:
        return None
    return ctk.CTkImage(light_image=picture, dark_image=picture, size=size)
