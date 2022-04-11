from PIL import Image
from typing import List


def white2transparent(img):
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img


def add_layer(background, foreground):
    return background


def merge(images: List[str], outfile: str):
    result = Image.open(images.pop(0))
    for image in images:
        image = Image.open(image)
        result.paste(image, (0, 0), image)
    result.save(outfile, optimize=True)
