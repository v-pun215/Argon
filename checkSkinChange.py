from PIL import Image
import imagehash
import requests
from io import BytesIO

def checkChangeSkin(url,  path):
    image1_url = url
    image2_path = path

    response = requests.get(image1_url)
    response.raise_for_status()
    image1 = Image.open(BytesIO(response.content))

    image2 = Image.open(image2_path)

    resize_dimensions = (64, 64)
    image1 = image1.resize(resize_dimensions, Image.Resampling.LANCZOS)
    image2 = image2.resize(resize_dimensions, Image.Resampling.LANCZOS)

    hash1 = imagehash.average_hash(image1)
    hash2 = imagehash.average_hash(image2)

    if hash1 == hash2:
        return False
    else:
        return True
