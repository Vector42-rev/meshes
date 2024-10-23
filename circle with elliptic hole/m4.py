import gmsh
import math
import numpy as np


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
gmsh.model.add("circle_with_ellipse_hole")

# Circle parameters
R1 = 2
order = 3
mesh_size = 0.5
# Ellipse parameters
a = 1.0  # Semi-major axis length
b = 0.5  # Semi-minor axis length
center_x, center_y = 0.0, 0.0

# Create points and geometry for the ellipse
num_points = 150  # Number of points to approximate the ellipse
ellipse_points = []
for i in range(num_points):
    angle = 2 * math.pi * i / num_points
    x = center_x + a * math.cos(angle)
    y = center_y + b * math.sin(angle)
    ellipse_points.append(gmsh.model.geo.addPoint(x, y, 0, mesh_size))

# Create closed spline for the ellipse
ellipse_lines = []
for i in range(num_points):
    ellipse_lines.append(gmsh.model.geo.addLine(ellipse_points[i], ellipse_points[(i + 1) % num_points]))

ellipse_curve_loop = gmsh.model.geo.addCurveLoop(ellipse_lines)

# Create points and geometry for the outer circle
center = gmsh.model.geo.addPoint(0, 0, 0, mesh_size)
circle_points = [gmsh.model.geo.addPoint(R1 * math.cos(2 * math.pi * j / 3), R1 * math.sin(2 * math.pi * j / 3), 0, mesh_size) for j in range(3)]
circle_lines = [gmsh.model.geo.addCircleArc(circle_points[j], center, circle_points[(j + 1) % 3]) for j in range(3)]
circle_curve_loop = gmsh.model.geo.addCurveLoop(circle_lines)

# Create surface with the circle as outer boundary and the ellipse as a hole
disk_with_hole = gmsh.model.geo.addPlaneSurface([circle_curve_loop, ellipse_curve_loop])

# Add physical groups for boundaries and surface
boundary = gmsh.model.addPhysicalGroup(1, circle_lines, 1)
nodes_loc = gmsh.model.addPhysicalGroup(2, [disk_with_hole], 1)

# Synchronize and generate mesh
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)

N, p, t, b = collect_node(order, nodes_loc, boundary)
gmsh.fltk.run()
gmsh.finalize()