from PIL import Image
from rembg import remove
import io
import secrets


async def resize_100(image):
    image = Image.open(io.BytesIO(image.content))
    image = image.resize((100, 100), Image.ANTIALIAS)
    image_name = secrets.token_hex(8)
    image.save(f"photo/{image_name}.png",
               format="PNG")
    return image_name


async def resize_512(image):
    image = Image.open(io.BytesIO(image.content))
    width, height = image.size

    if width > height:
        new_width = 512
        new_height = int(new_width * (height / width))
        if new_height > 512:
            new_height = new_height - (new_height - 512)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)
    elif height > width:
        width, height = image.size
        new_height = 512
        new_width = int(new_height * (width / height))
        if new_width > 512:
            new_width = new_width - (new_width - 512)

        image = image.resize((new_width, new_height), Image.ANTIALIAS)
    else:
        image = image.resize((512, 512), Image.ANTIALIAS)
    image_name = secrets.token_hex(8)
    image.save(f"photo/{image_name}.png",
               format="PNG")
    return image_name


async def resize_custom(image, x_ax, y_ax):
    image = Image.open(io.BytesIO(image.content))
    image = image.resize((x_ax, y_ax), Image.ANTIALIAS)
    image_name = secrets.token_hex(8)
    image.save(f"photo/{image_name}.png",
               format="PNG")
    return image_name


async def remove_bg(image):
    image = Image.open(io.BytesIO(image.content))
    output_image = remove(image)
    image_name = secrets.token_hex(8)
    output_image.save(f"photo/{image_name}.png",
                      format="PNG")
    return image_name
