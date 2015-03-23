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

def zip_from_image(file, sizes):
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
             print image_name
             image_path = os.path.join(dir, 'temp', rand, image_name)
             print image_path
             img = ResizeToFit(width=size, upscale=True).process(image)
             print img
             img.save(image_path)
             print img
             print img.close()
             print zipfile.write(image_path, image_name)
             print os.remove(image_path)
    return zip_path


@app.route("/")
def index():
    return """
<!doctype html>
<html>
<head>
</head>
<body>
    <h1>Quick Dallas Morning News photo resizer</h1>
    <p>
      <form action="/zip" method="post" enctype="multipart/form-data">
        Minimum size:      <input type="text" name="minSize" /><br>
        Maximum size:  <input type="text" name="maxSize" /><br>
        Steps:  <input type="text" name="sizeSteps" /><br>
        File: <input type="file" name="photo" /><br>
        <input type="submit" value="Start upload" /><br>
      </form>
</body>
</html>
"""

@app.route("/zip", methods = ['POST',])
def make_zip_file():
    f = request.files['photo']
    min_size = request.form['minSize']
    max_size = request.form['maxSize']
    size_steps = request.form['sizeSteps']
    sizes = image_sizes(min_size, max_size, size_steps)
    zipfile = zip_from_image(f, sizes)
    file_path, file_name = os.path.split(zipfile)
    return send_file(zipfile, as_attachment=True,
        attachment_filename=file_name)


if __name__ == "__main__":
    app.debug = True
    app.run()
