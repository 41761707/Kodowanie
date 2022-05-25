from PIL import Image
from sys import argv

Image.open(argv[1]).save(argv[2])