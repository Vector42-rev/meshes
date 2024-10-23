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
    # Get element information
    e = s.getElements(2, 1)
    e1 = e[2][0]
    t = [e1[i:i + nodes_per_element] for i in range(0, len(e1), nodes_per_element)]
    # Get boundary nodes
    b = list(s.getNodesForPhysicalGroup(1, boundary)[0])
    return N, P, t, b


gmsh.initialize()
gmsh.model.add("ellipse_with_hole")

# Mesh parameters
order = 1
mesh_size = 0.4

# Ellipse parameters
a1 = 1.0  # Outer ellipse semi-major axis
b1 = 0.5  # Outer ellipse semi-minor axis
a0 = 1.443375672  # Inner ellipse semi-major axis
b0 = 1.154700538  # Inner ellipse semi-minor axis
center_x, center_y = 0.0, 0.0

# Add points for outer ellipse
center = gmsh.model.geo.addPoint(center_x, center_y, 0)

# Define points on the outer ellipse
p1_outer = gmsh.model.geo.addPoint(center_x + a1, center_y, 0, mesh_size)
p2_outer = gmsh.model.geo.addPoint(center_x, center_y - b1, 0, mesh_size)
p3_outer = gmsh.model.geo.addPoint(center_x - a1, center_y, 0, mesh_size)
p4_outer = gmsh.model.geo.addPoint(center_x, center_y + b1, 0, mesh_size)

# Define points on the inner ellipse
p1_inner = gmsh.model.geo.addPoint(center_x + a0, center_y, 0, mesh_size)
p2_inner = gmsh.model.geo.addPoint(center_x, center_y - b0, 0, mesh_size)
p3_inner = gmsh.model.geo.addPoint(center_x - a0, center_y, 0, mesh_size)
p4_inner = gmsh.model.geo.addPoint(center_x, center_y + b0, 0, mesh_size)

# Outer ellipse arcs
outer_arc1 = gmsh.model.geo.addEllipseArc(p1_outer, center, p2_outer, p2_outer)
outer_arc2 = gmsh.model.geo.addEllipseArc(p2_outer, center, p3_outer, p3_outer)
outer_arc3 = gmsh.model.geo.addEllipseArc(p3_outer, center, p4_outer, p4_outer)
outer_arc4 = gmsh.model.geo.addEllipseArc(p4_outer, center, p1_outer, p1_outer)

# Inner ellipse arcs
inner_arc1 = gmsh.model.geo.addEllipseArc(p1_inner, center, p2_inner, p2_inner)
inner_arc2 = gmsh.model.geo.addEllipseArc(p2_inner, center, p3_inner, p3_inner)
inner_arc3 = gmsh.model.geo.addEllipseArc(p3_inner, center, p4_inner, p4_inner)
inner_arc4 = gmsh.model.geo.addEllipseArc(p4_inner, center, p1_inner, p1_inner)

# Create curve loops for the outer and inner ellipses
outer_ellipse_curve_loop = gmsh.model.geo.addCurveLoop([outer_arc1, outer_arc2, outer_arc3, outer_arc4])
inner_ellipse_curve_loop = gmsh.model.geo.addCurveLoop([inner_arc1, inner_arc2, inner_arc3, inner_arc4])

# Create surface with the inner ellipse as a hole
disk_with_hole = gmsh.model.geo.addPlaneSurface([outer_ellipse_curve_loop, inner_ellipse_curve_loop])

# Add physical groups for boundaries and surface
outer_boundary = gmsh.model.addPhysicalGroup(1, [outer_arc1, outer_arc2, outer_arc3, outer_arc4], 1)
inner_boundary = gmsh.model.addPhysicalGroup(1, [inner_arc1, inner_arc2, inner_arc3, inner_arc4], 2)
surface_group = gmsh.model.addPhysicalGroup(2, [disk_with_hole], 1)

# Synchronize and generate mesh
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)

# Collect nodes for both the inner and outer boundaries
N, p, t, outer_boundary_nodes = collect_node(order, surface_group, outer_boundary)
_, _, _, inner_boundary_nodes = collect_node(order, surface_group, inner_boundary)


gmsh.fltk.run()
gmsh.finalize()