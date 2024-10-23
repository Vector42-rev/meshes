

import gmsh

import sys

gmsh.initialize()

gmsh.model.add("square")



lc=0.5

order=3

gmsh.model.geo.addPoint(0,0,0,lc,1)

gmsh.model.geo.addPoint(2,0,0,lc,2)

gmsh.model.geo.addPoint(2,2,0,lc,3)

gmsh.model.geo.addPoint(0,2,0,lc,4)



gmsh.model.geo.addLine(1,2,1)

gmsh.model.geo.addLine(2,3,2)

gmsh.model.geo.addLine(3,4,3)

gmsh.model.geo.addLine(4,1,4)



gmsh.model.geo.addCurveLoop([1,2,3,4],1)

gmsh.model.geo.addPlaneSurface([1],1)

gmsh.model.addPhysicalGroup(1,[1,2,3,4],10)

gmsh.model.addPhysicalGroup(2,[1],56)

gmsh.model.geo.synchronize()



gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)


if '-nopopup' not in sys.argv:

	gmsh.fltk.run()

gmsh.finalize()