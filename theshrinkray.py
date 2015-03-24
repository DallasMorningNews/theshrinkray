#!/usr/bin/env python
from PIL import Image
from pilkit.processors import ResizeToFit
from flask import Flask, request, send_from_directory, send_file
import os
from tempfile import TemporaryFile, NamedTemporaryFile
from zipfile import ZipFile
import random, string
from pprint import pprint
from werkzeug import secure_filename


app = Flask(__name__)


dir = os.path.dirname(__file__)


def image_sizes(min, max, steps):
    sizes = []
    max = float(max)
    min = float(min)
    steps = int(steps)
    step_size = (max - min)/(steps - 1)
    for step in range(0, steps):
        size = step * step_size + min
        sizes.append(int(size))
    return sizes

def zip_from_image(file, sizes, quality=75):
    rand = ''.join(random.sample(string.letters, 15))
    os.mkdir(os.path.join(dir, 'temp',rand))
    file_path, file_name = os.path.split(file.filename)
    base, ext = os.path.splitext(file_name)
    image_name = "{}_{}{}".format(base, 'orig', ext)
    image_path = os.path.join(dir, 'temp', rand, image_name)
    f = file.save(image_path)
    # secure_path = os.path.join(dir, 'temp', rand, secure_filename(file_name))
    # f = file.save(secure_path)
    zip_name = "{}.zip".format(base)
    zip_path = os.path.join(dir, 'temp', rand, zip_name)
    image = Image.open(image_path)
    print image_path, zip_path
    # print zip_path
    with ZipFile(zip_path, 'w') as zipfile:
        zipfile.write(image_path, image_name)
        os.remove(image_path)
        for size in sizes:
            image_name = "{}_{}{}".format(base, size, ext)
            image_path = os.path.join(dir, 'temp', rand, image_name)
            img = ResizeToFit(width=size, upscale=True).process(image)
            img.save(image_path, progressive=True, exif="", optimize=True,
                quality = quality, icc_profile=img.info.get('icc_profile'))
            img.close()
            zipfile.write(image_path, image_name)
            os.remove(image_path)
    return zip_path


def zip_from_zip(file, sizes, quality=75):
    rand = ''.join(random.sample(string.letters, 15))
    os.mkdir(os.path.join(dir, 'temp',rand))


    file_path, file_name = os.path.split(file.filename)
    base, ext = os.path.splitext(file_name)
    image_name = "{}_{}{}".format(base, 'orig', ext)
    image_path = os.path.join(dir, 'temp', rand, image_name)
    f = file.save(image_path)
    # secure_path = os.path.join(dir, 'temp', rand, secure_filename(file_name))
    # f = file.save(secure_path)
    zip_name = "{}.zip".format(base)
    zip_path = os.path.join(dir, 'temp', rand, zip_name)
    image = Image.open(image_path)
    print image_path, zip_path
    # print zip_path
    with ZipFile(zip_path, 'w') as zipfile:
        zipfile.write(image_path, image_name)
        os.remove(image_path)
        for size in sizes:
            image_name = "{}_{}{}".format(base, size, ext)
            image_path = os.path.join(dir, 'temp', rand, image_name)
            img = ResizeToFit(width=size, upscale=True).process(image)
            img.save(image_path, progressive=True, exif="", optimize=True,
                quality = quality, icc_profile=img.info.get('icc_profile'))
            img.close()
            zipfile.write(image_path, image_name)
            os.remove(image_path)
    return zip_path
    # rand = ''.join(random.sample(string.letters, 15))
    # os.mkdir(os.path.join(dir, 'temp',rand))
    # file_path, file_name = os.path.split(file.filename)
    # base, ext = os.path.splitext(file_name)
    # image_name = "{}_{}{}".format(base, 'orig', ext)
    # image_path = os.path.join(dir, 'temp', rand, image_name)
    # f = file.save(image_path)
    # # secure_path = os.path.join(dir, 'temp', rand, secure_filename(file_name))
    # # f = file.save(secure_path)
    # zip_name = "{}.zip".format(base)
    # zip_path = os.path.join(dir, 'temp', rand, zip_name)
    # image = Image.open(image_path)
    # print image_path, zip_path
    # # print zip_path
    # with ZipFile(zip_path, 'w') as zipfile:
    #     zipfile.write(image_path, image_name)
    #     os.remove(image_path)
    #     for size in sizes:
    #         image_name = "{}_{}{}".format(base, size, ext)
    #         image_path = os.path.join(dir, 'temp', rand, image_name)
    #         img = ResizeToFit(width=size, upscale=True).process(image)
    #         img.save(image_path, progressive=True, exif="", optimize=True, quality = 75)
    #         img.close()
    #         zipfile.write(image_path, image_name)
    #         os.remove(image_path)
    # return zip_path


@app.route("/")
def index():
    return send_file('static/index.html')

@app.route("/zip", methods = ['POST',])
def make_zip_file():
    f = request.files['photo']
    min_size = float(request.form['minSize'])
    max_size = float(request.form['maxSize'])
    size_steps = int(request.form['sizeSteps'])
    quality = int(request.form['quality'])
    sizes = image_sizes(min_size, max_size, size_steps)
    zipfile = zip_from_image(f, sizes, quality=quality)
    file_path, file_name = os.path.split(zipfile)
    return send_file(zipfile, as_attachment=True,
        attachment_filename=file_name)


if __name__ == "__main__":
    app.debug = True
    app.run()
