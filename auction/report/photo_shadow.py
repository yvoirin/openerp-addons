# -*- encoding: utf-8 -*-

def convert_catalog(from_file, to_file, size=220) :
    return __convert(from_file, to_file, size)

def convert(from_file, to_file):
    size = 95
    __convert(from_file, to_file, size=95)

def __convert(from_file, to_file, size=95):
    import Image, ImageDraw, ImageFilter
    im = Image.open(from_file)
    if float(im.size[1]/im.size[0])>2:
        im = im.resize((im.size[0]*size/im.size[1], size))
    else:
        im = im.resize((size,im.size[1]*size/im.size[0]))
    newimg = Image.new('RGB', (im.size[0]+8,im.size[1]+8), (255,255,255) )

    draw = ImageDraw.Draw(newimg)
    draw.rectangle((6, im.size[1]-5, im.size[0], im.size[1]+5), fill=(90,90,90))
    draw.rectangle((im.size[0]-5, 6, im.size[0]+5, im.size[1]), fill=(90,90,90))
    del draw 

    newimg = newimg.filter(ImageFilter.BLUR)
    newimg = newimg.filter(ImageFilter.BLUR)
    newimg = newimg.filter(ImageFilter.BLUR)

    newimg.paste(im, (0,0))
    draw = ImageDraw.Draw(newimg)
    draw.rectangle((0, 0, im.size[0], im.size[1]), outline=(0,0,0))
    del draw 
    to_fp = file(to_file, 'wb')
    newimg.save(to_fp, "JPEG")
    to_fp.close()
    res = newimg.size
    del im
    del newimg
    return res
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

