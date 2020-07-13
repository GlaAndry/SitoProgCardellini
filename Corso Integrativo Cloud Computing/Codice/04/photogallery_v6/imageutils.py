from PIL import Image, ImageEnhance, ImageFilter

def apply_filters (filename, filters, max_size=None):
    img = Image.open(filename)

    for f in filters:
        if f == "Black and White" or f == "bw":
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(0.0)
        elif f == "Blur":
            img = img.filter(ImageFilter.GaussianBlur(radius=50))

    if max_size != None:
        size = (max_size, max_size)
        img.thumbnail(size, Image.ANTIALIAS)

    img.save(filename, format="PNG")
