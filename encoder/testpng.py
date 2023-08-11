import os
from PIL import Image

Image.open('out/2.jpeg').resize((4000, 3000)).save('out/2.png')
os.remove('out/2.jpeg')
