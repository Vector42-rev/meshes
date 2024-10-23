import gmsh
import numpy as np
import math

def collect_node(order, nodes_loc, boundary):
    s = gmsh.model.mesh
    nodes_per_element = int(((order + 1) * (order + 2)) / 2)
    # Get node information
    Nodes = s.getNodesForPhysicalGroup(2, nodes_loc)
    N = len(Nodes[0])
    P1 = np.array(Nodes[1])
    P = [P1[i:i + 3] for i in range(0, len(P1), 3)]
    print("N= ", N)
    #print("P= ")
    #for i, node_coords in enumerate(P):
    #    print(f"{i + 1} {node_coords}")
    # Get element information
    e = s.getElements(2, 1)
    e1 = e[2][0]
    t = [e1[i:i + nodes_per_element] for i in range(0, len(e1), nodes_per_element)]
    #print("t= ")
    #print(t)
    # Get boundary nodes
    b = list(s.getNodesForPhysicalGroup(1, boundary)[0])
    #print("b= ")
    #print(b)
    return N, P, t, b

gmsh.initialize()
gmsh.model.add("circle")

order = 1
mesh_size = 0.5
R1 = 1.0

center = gmsh.model.geo.addPoint(0, 0, 0, mesh_size, 10)
points = [gmsh.model.geo.addPoint(R1 * math.cos(2 * math.pi * j / 3),R1 * math.sin(2 * math.pi * j / 3), 0, mesh_size) for j in range(3)]
lines = [gmsh.model.geo.addCircleArc(points[j], center, points[(j + 1) % 3]) for j in range(3)]
curveloop = gmsh.model.geo.addCurveLoop([lines[0], lines[1], lines[2]])
disk = gmsh.model.geo.addPlaneSurface([curveloop])
boundary = gmsh.model.addPhysicalGroup(1, lines, 1)
nodes_loc = gmsh.model.addPhysicalGroup(2, [disk], 1)
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)

gmsh.fltk.run()
N, p, t, b = collect_node(order, nodes_loc, boundary)
gmsh.finalize()