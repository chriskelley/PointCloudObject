PointCloudObject
================

Plugin to create a "PointCloudObject" in Cinema 4D to import and display point clouds.


Usage
--------

Data is expected in a text file, one entry per line, space delimited, with the following format:

posX posY posZ colorR colorG colorB nrmX nrmY nrmZ

File should be space-delimited and color values should be 0-255.

Currently this is a viewport-only plugin, point cloud is not renderable.  Only used for reference. 


TODO
--------

- options for delimeter
- options for inclusion/exclusion of each data object (pos, color, normal)
- option for color range type
- option to make renderable
