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
import io
import shutil

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

def img_src_formatter(info):
	"""
	Takes a  tuple ('name', width) and generates
	the srclist item for a responsive image tag.
	"""
	return "{} {}w".format(info[0], info[1])


def take_closest(num,collection):
	"""
	Thanks for the advice stack overflow:
	http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
	"""
	return min(collection,key=lambda x:abs(x-num))


def zip_from_image(file, sizes, quality=75, default_size=1600, alt_text="YOU MUST ENTER ALT TEXT", image_tag_path="images/"):
    rand = ''.join(random.sample(string.letters, 15))
    os.mkdir(os.path.join(dir, 'temp',rand))
    file_path, file_name = os.path.split(file.filename)
    base, ext = os.path.splitext(file_name)
    base = base.lower()
    ext = ext.lower()
    image_name = "{}_{}{}".format(base, 'orig', ext)
    image_path = os.path.join(dir, 'temp', rand, image_name)
    f = file.save(image_path)
    zip_name = "{}.zip".format(base).lower()
    zip_path = os.path.join(dir, 'temp', rand, zip_name)
    image = Image.open(image_path)
    img_srcset_tuples = []
    with ZipFile(zip_path, 'w') as zipfile:
    	zipfile.write(image_path, image_name)
    	os.remove(image_path)
        for size in sizes:
            image_name = "{}_{}{}".format(base, size, ext)
            img_srcset_tuples.append(("{}{}".format(image_tag_path, image_name), size))
            image_path = os.path.join(dir, 'temp', rand, image_name)
            img = ResizeToFit(width=size, upscale=True).process(image)
            img.save(image_path, progressive=True, exif="", optimize=True,
                quality = quality, icc_profile=img.info.get('icc_profile'))
            img.close()
            zipfile.write(image_path, image_name)
            os.remove(image_path)
        # src_file = open(os.path.join(dir, 'temp', rand, 'img_tag.txt')
		#  src_file.write('<img srcset="')
        img_srcset_strings = map(img_src_formatter, img_srcset_tuples)
        best_size = take_closest(default_size, sizes)
        img_src_string = img_srcset_tuples[sizes.index(best_size)][0]
        img_tag_html = '<img srcset="{}" src="{}" sizes="(min-width: 1px) 100vw" alt="{}">'.format(', '.join(img_srcset_strings), img_src_string, alt_text)
        img_tag_html_file_name = os.path.join(dir, 'temp', rand, 'html.txt')
        img_tag_html_file = open(img_tag_html_file_name, 'w')
        img_tag_html_file.write(img_tag_html)
        img_tag_html_file.close()
        zipfile.write(img_tag_html_file_name, 'html.txt')
    return zip_path



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
	bytes = ""
	with open(zipfile, 'r') as zipr:
		bytes = io.BytesIO(zipr.read())
	shutil.rmtree(file_path)
	return send_file(bytes, as_attachment=True,	attachment_filename=file_name)

app.debug = False

if __name__ == "__main__":
    app.debug = True
    app.run()
