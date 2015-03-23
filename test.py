import os, shutil
import theshrinkray
import unittest
import tempfile
import json
from PIL import Image



def get_image_file():
    """
    See also:
    http://en.wikipedia.org/wiki/Lenna
    http://sipi.usc.edu/database/database.php?volume=misc&image=12
    """
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'test_files', 'lenna.png')
    return open(path, 'r+b')

def create_image():
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'test_files', 'lenna.png')
    return Image.open(path)




class ShrinkRayTestCase(unittest.TestCase):

    def setUp(self):
        if not os.access('temp', os.F_OK):
            os.mkdir('temp')
        self.app = theshrinkray.app.test_client()

    def tearDown(self):
        pass
        # shutil.rmtree('temp')
        # os.mkdir('temp')

    def test_right_sizes(self):
        shrink_sizes = theshrinkray.image_sizes(100, 200, 2)
        assert shrink_sizes == [100, 200]
        shrink_sizes = theshrinkray.image_sizes(100, 200, 3)
        assert shrink_sizes == [100, 150, 200]

    def test_make_zipfile_from_image_creates_file(self):
        img = get_image_file()
        sizes = theshrinkray.image_sizes(100, 2000, 4)
        zipname = theshrinkray.zip_from_image(img, sizes)
        assert os.access(zipname, os.F_OK) is True


if __name__ == '__main__':
    unittest.main()
