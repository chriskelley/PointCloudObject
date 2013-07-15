"""
PointCloudObject
Copyright: Christopher Kelley
Written for CINEMA 4D R13.058
"""

import os
import math
import sys
import random
import c4d

from c4d import plugins, utils, bitmaps, gui


PLUGIN_ID = 1030817


class PointCloudObject(plugins.ObjectData):

    def GetVirtualObjects(self, op, hierarchyhelp):
        dirty = op.CheckCache(hierarchyhelp) or op.IsDirty(c4d.DIRTY_DATA)
        if dirty is False: return op.GetCache(hierarchyhelp)

    def Message(self, op, type, data):
        if type == c4d.MSG_DESCRIPTION_COMMAND:
            if data['id'][0].id == c4d.POINTCLOUDOBJECT_LOADBTN:
                self.LoadData(op)
        return True

    def Init(self, op):
        self.InitAttr(op, bool, [c4d.POINTCLOUDOBJECT_INVERTY])
        self.InitAttr(op, float, [c4d.POINTCLOUDOBJECT_POINTSIZE])
        self.InitAttr(op, float, [c4d.POINTCLOUDOBJECT_DENSITY])

        op[c4d.POINTCLOUDOBJECT_INVERTY] = True
        op[c4d.POINTCLOUDOBJECT_POINTSIZE] = 1.0
        op[c4d.POINTCLOUDOBJECT_DENSITY] = 0.5

        self.pvec = []
        self.cvec = []
        self.pointcount = 0
        self.scale = 10
        self.initialStep = 100
        self.particleStep = 0
        self.initialPointCeiling = 10000.0
        self.colordepth = 255
        self.pointsize = 1
        self.dataIsLoaded = False

        self.boundingBox = dict.fromkeys(['min_x', 'min_y', 'min_z', 'max_x', 'max_y', 'max_z'], 0)

        return True

    def GetDimension(self, op, mp, rad):
        """
        (i) When the method runs without a raised exception
        mp and rad will be internally copied, otherwise they
        are ignored.
        """
        mp.x = self.boundingBox['max_x'] - self.boundingBox['min_x']
        mp.y = self.boundingBox['max_y'] - self.boundingBox['min_y']
        mp.z = self.boundingBox['max_z'] - self.boundingBox['min_z']

        return

    def Draw(self, op, drawpass, bd, bh):
        if drawpass == c4d.DRAWPASS_OBJECT:
            if self.dataIsLoaded:
                bd.SetMatrix_Matrix(None, bh.GetMg())

                stepsize = int(self.pointcount / (self.pointcount * op[c4d.POINTCLOUDOBJECT_DENSITY]))

                for i in xrange(0, self.pointcount, stepsize):
                    self.CreatePoint(bd, self.pvec[i], self.cvec[i], op[c4d.POINTCLOUDOBJECT_POINTSIZE])

        return c4d.DRAWRESULT_OK

    def LoadData(self, op, fname=""):
        self.pvec, self.cvec, self.pointcount = [], [], 0
        fname = "/Users/chriskelley/Downloads/PointCloudReduced.txt"
        with open(fname) as f:
            for i, l in enumerate(f):
                if i % self.initialStep == 0:

                    d = self.ParseLine(l)  # returns [posx, posy, posz, colorx, colory, colorz]

                    if op[c4d.POINTCLOUDOBJECT_INVERTY]:
                        d[1] = d[1] * -1

                    self.pvec.append(c4d.Vector(d[0], d[1], d[2]))
                    self.cvec.append(c4d.Vector(d[3], d[4], d[5]))

                    self.UpdateBoundingBox(d)

                    self.pointcount += 1

        if self.pointcount > 0:
            self.particleStep = self.pointcount - (self.pointcount * (self.initialPointCeiling / self.pointcount))
            op[c4d.POINTCLOUDOBJECT_DENSITY] = self.initialPointCeiling / self.pointcount
            self.dataIsLoaded = True

        return True

    def ParseLine(self, line, delim=" "):
        d = [float(i) for i in line.split(delim)]  # px, py, pz, cr, cg, cb, nx, ny, nz
        p = [i*self.scale for i in [d[0], d[1], d[2]]]  # position
        c = [i/self.colordepth for i in [d[3], d[4], d[5]]]  # colors

        return p + c

    def CreatePoint(self, bd, pvec, cvec, size=1):
        v1 = c4d.Vector(1, 0, 0)  # x-axis
        v2 = c4d.Vector(0, 1, 0)  # y-axis
        v3 = c4d.Vector(0, 0, 1)  # z-axis
        m = c4d.Matrix(pvec, v1, v2, v3)

        bd.DrawBox(m, size, cvec, False)

    def UpdateBoundingBox(self, dim):
        if dim[0] < self.boundingBox['min_x']:
            self.boundingBox['min_x'] = dim[0]

        if dim[1] < self.boundingBox['min_y']:
            self.boundingBox['min_y'] = dim[1]

        if dim[2] < self.boundingBox['min_z']:
            self.boundingBox['min_z'] = dim[2]

        if dim[0] > self.boundingBox['max_x']:
            self.boundingBox['max_x'] = dim[0]

        if dim[1] > self.boundingBox['max_y']:
            self.boundingBox['max_y'] = dim[1]

        if dim[2] > self.boundingBox['max_z']:
            self.boundingBox['max_z'] = dim[2]

        return True



if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    icon = bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(dir, "res", "pointcloudobject.tif"))
    plugins.RegisterObjectPlugin(id=PLUGIN_ID, str="PointCloudObject", g=PointCloudObject, description="opointcloudobject", icon=icon, info=c4d.OBJECT_GENERATOR)
