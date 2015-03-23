#!/usr/bin/env python
from PIL import Image
from pilkit.processors import ResizeToFit
from flask import Flask
import os
from zipfile import ZipFile
import random, string


app = Flask(__name__)


dir = os.path.dirname(__file__)


def image_sizes(min, max, steps):
    sizes = []
    max = float(max)
    min = float(min)
    step_size = (max - min)/(steps - 1)
    for step in range(0, steps):
        size = step * step_size + min
        sizes.append(int(size))
    return sizes

# def resize_from_sizes(file, sizes):
#     image = Image.open(file)
#     path, file_name = os.path.split(file.name)
#     base, ext = os.path.splitext(file_name)
#     # print path, base, ext
#     image_name = "{}{}".format(base, ext)
#     rand = ''.join(random.sample(string.letters, 15))
#     os.mkdir(os.path.join('temp',rand))
#     filepath = os.path.join('temp', rand, image_name)
#     image.save(filepath)
#     images = [filepath]
#     for size in sizes:
#         image_name = "{}_{}{}".format(base, size, ext)
#         filepath = os.path.join('temp', rand, image_name)
#         img = ResizeToFit(width=size, upscale=True).process(image)
#         img.save(filepath)
#         img.close()
#         images.append(filepath)
#     image.close()
#     return images
#
# def zip_from_filenames(images):
#     rand = ''.join(random.sample(string.letters, 15))
#     path, file_name = os.path.split(images[0])
#     base, ext = os.path.splitext(file_name)
#     zip_name = "{}.zip".format(base)
#     os.mkdir(os.path.join('temp',rand))
#     zip_path = os.path.join('temp', rand, zip_name)
#     with ZipFile(zip_path, 'w') as zipfile:
#         for image in images:
#             path, basename = os.path.split(image)
#             zipfile.write(image, basename)
#             os.remove(image)
#     return zip_path


def zip_from_image(file, sizes):
    rand = ''.join(random.sample(string.letters, 15))
    os.mkdir(os.path.join(dir, 'temp',rand))
    file_path, file_name = os.path.split(file.name)
    base, ext = os.path.splitext(file_name)
    # image = Image.open(path)
    zip_name = "{}.zip".format(base)
    zip_path = os.path.join(dir, 'temp', rand, zip_name)
    image = Image.open(file)
    print zip_path
    with ZipFile(zip_path, 'w') as zipfile:
        image_name = "{}_{}{}".format(base, 'orig', ext)
        zipfile.write(file.name, image_name)
        for size in sizes:
             image_name = "{}_{}{}".format(base, size, ext)
             image_path = os.path.join(dir, 'temp', rand, image_name)
             img = ResizeToFit(width=size, upscale=True).process(image)
             img.save(image_path)
             img.close()
             zipfile.write(image_path, image_name)
             os.remove(image_path)
    return zip_path
