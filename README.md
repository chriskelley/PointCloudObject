PointCloudObject
================

Plugin to create a "PointCloudObject" in Cinema 4D to import and display point clouds.


Usage
--------

Data is expected in a text file in with the following format:
PositionX PositionY PositionZ ColorR ColorG ColorB NormalX NormalY NormalZ

File should be space-delimited and color values should be 0-255.

Currently this is a viewport-only plugin, point cloud is not renderable.  Only used for reference. 


TODO
--------

- Add options for delimeter
- Hook up file loading
- Make renderable
