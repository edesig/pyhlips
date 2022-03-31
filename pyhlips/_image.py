from PIL import Image

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

def add(img1, img2, out_file):
    background = white2transparent(Image.open(img1))
    foreground = white2transparent(Image.open(img2))

    background.paste(foreground, (0, 0), foreground)
    background.save(out_file, optimize=True)
