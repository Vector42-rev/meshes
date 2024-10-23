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
gmsh.model.add("circle_with_2_circular_holes")
mesh_size=0.5
order=1
center_x, center_y = 0.0, 0.0
c1=0.3
c2=0.4
r=1

center1 = gmsh.model.geo.addPoint(center_x, center_y, 0, mesh_size)
circle_points1 = [gmsh.model.geo.addPoint(r* math.cos(2 * math.pi * j / 3), r * math.sin(2 * math.pi * j / 3), 0, mesh_size) for j in range(3)]
circle_lines1 = [gmsh.model.geo.addCircleArc(circle_points1[j], center1, circle_points1[(j + 1) % 3]) for j in range(3)]


center2 = gmsh.model.geo.addPoint(center_x-0.5, center_y, 0, mesh_size)
circle_points2 = [gmsh.model.geo.addPoint((center_x-0.5)+c1* math.cos(2 * math.pi * j / 3), center_y+c1 * math.sin(2 * math.pi * j / 3), 0, mesh_size) for j in range(3)]
circle_lines2 = [gmsh.model.geo.addCircleArc(circle_points2[j], center2, circle_points2[(j + 1) % 3]) for j in range(3)]

center3 = gmsh.model.geo.addPoint(center_x+0.5, center_y, 0, mesh_size)
circle_points3 = [gmsh.model.geo.addPoint(center_x+0.5+c2* math.cos(2 * math.pi * j / 3), center_y+c2 * math.sin(2 * math.pi * j / 3), 0, mesh_size) for j in range(3)]
circle_lines3 = [gmsh.model.geo.addCircleArc(circle_points3[j], center3, circle_points3[(j + 1) % 3]) for j in range(3)]



circle_curve_loop1 = gmsh.model.geo.addCurveLoop(circle_lines1)
circle_curve_loop2 = gmsh.model.geo.addCurveLoop(circle_lines2)
circle_curve_loop3 = gmsh.model.geo.addCurveLoop(circle_lines3)

circle_with_holes = gmsh.model.geo.addPlaneSurface([circle_curve_loop1,circle_curve_loop2,circle_curve_loop3])


outer_boundary = gmsh.model.addPhysicalGroup(1, circle_lines1, 1)
inner_boundary1 = gmsh.model.addPhysicalGroup(1, circle_lines2, 2)
inner_boundary2 = gmsh.model.addPhysicalGroup(1, circle_lines3, 3)
surface_group = gmsh.model.addPhysicalGroup(2, [circle_with_holes], 1)

gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)

N, p, t, outer_boundary_nodes = collect_node(order, surface_group, outer_boundary)
_, _, _, inner_boundary_nodes1 = collect_node(order, surface_group, inner_boundary1)
_, _, _, inner_boundary_nodes2 = collect_node(order, surface_group, inner_boundary2)

merged_nodes = np.concatenate((inner_boundary_nodes1, outer_boundary_nodes,inner_boundary_nodes1)).astype(int)
b = np.sort(merged_nodes)
print(b)
gmsh.fltk.run()
gmsh.finalize()