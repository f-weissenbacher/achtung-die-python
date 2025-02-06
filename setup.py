import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
   name='achtung-die-python',
   version='1.0.0',
   description='Python implementation of Achtung-die-Kurve game',
   long_description=read("README.md"),
   author='Fabian Weissenbacher',
   #author_email='fabian.weissenbacher@tugraz.at',
   package_dir={"":"src"},
   install_requires=['numpy',
                     'pandas'],
   extras_require={
      'gui': ['pygame'],
   },
   #entry_points={
   #   'console_scripts': [
   #      "video-from-frames = interact_utils.cmdline.video_from_frames:run",
   #      "show-birdseye-view = interact_utils.cmdline.show_birdseye_view:run",
   #      "overlay-video-with-timestamps = interact_utils.cmdline.overlay_video_with_timestamps:run",
   #   ]
   #}
)
