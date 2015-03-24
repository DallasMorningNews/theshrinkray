![Shrinkray logo](/static/logo.png "The Shrinkray")
## The Shrinkray

The Shrinkray is a tool for tasking on image and creating a bunch of sizes, generally this will be for responsive design purposes.

It's based on Flask and written by Daniel Lathrop. You can see it at work
at http://theshrinkray.herokuapp.com.

Current features:

* supports any format supported by the Python Imaging Library
* supports customizable quality levels for JPGs
* strips exif data (because, that's why)
* upscales images if they're smaller than max size
* returns the original along with the sized versions

For future features/plans/requests please see the issues. The main ones under consideration for 2.0 are: batch resize on groups of images and conversion to a Flask blueprint so it can be used inside other programs.

--

&copy; copyright 2015 by The Dallas Morning News (@dallasnews)  
written by Daniel Lathrop (@lathropd)  
logo by Troy Oxford (@TroyOxford)  
