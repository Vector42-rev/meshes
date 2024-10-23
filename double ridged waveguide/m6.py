import gmsh
import numpy as np


def collect_node(order, nodes_loc, boundary):
    s = gmsh.model.mesh
    nodes_per_element = int(((order + 1) * (order + 2)) / 2)

    # Get node information for the surface (2D elements)
    Nodes = s.getNodesForPhysicalGroup(2, nodes_loc)
    N = len(Nodes[0])  # List of node tags for the physical group
    P1 = np.array(Nodes[1])  # Corresponding node coordinates
    P = [P1[i:i + 3] for i in range(0, len(P1), 3)]  # Break the list into (x, y, z) triplets

    print("N= ", N)

    # Get element information for the 2D surface
    e = s.getElements(2, 1)
    if e[2]:
        e1 = e[2][0]
        t = [e1[i:i + nodes_per_element] for i in range(0, len(e1), nodes_per_element)]
    else:
        t = []

    # Get boundary nodes (1D elements)
    boundary_nodes = list(s.getNodesForPhysicalGroup(1, boundary)[0])

    return N, P, t, boundary_nodes


gmsh.initialize()
gmsh.model.add("Double Ridged Waveguide")

order = 3
mesh_size = 0.027
l1 = 0.508
l2 = 0.3683
l3 = 0.254
l4 = 1.016

# Defining the geometry points
J = gmsh.model.geo.addPoint(0, 0, 0, mesh_size)
I = gmsh.model.geo.addPoint(l3, 0, 0, mesh_size)
H = gmsh.model.geo.addPoint(l3, -l2, 0, mesh_size)
G = gmsh.model.geo.addPoint(l3 + l1, -l2, 0, mesh_size)
F = gmsh.model.geo.addPoint(l3 + l1, -l2 + l4, 0, mesh_size)
E = gmsh.model.geo.addPoint(l3, -l2 + l4, 0, mesh_size)
D = gmsh.model.geo.addPoint(l3, -l2 + l4 - l2, 0, mesh_size)
C = gmsh.model.geo.addPoint(0, -l2 + l4 - l2, 0, mesh_size)
B = gmsh.model.geo.addPoint(0, -l2 + l4, 0, mesh_size)
A = gmsh.model.geo.addPoint(-l1, -l2 + l4, 0, mesh_size)
L = gmsh.model.geo.addPoint(-l1, -l2, 0, mesh_size)
K = gmsh.model.geo.addPoint(0, -l2, 0, mesh_size)

# Defining the lines
JI = gmsh.model.geo.addLine(J, I)
IH = gmsh.model.geo.addLine(I, H)
HG = gmsh.model.geo.addLine(H, G)
GF = gmsh.model.geo.addLine(G, F)
FE = gmsh.model.geo.addLine(F, E)
ED = gmsh.model.geo.addLine(E, D)
DC = gmsh.model.geo.addLine(D, C)
CB = gmsh.model.geo.addLine(C, B)
BA = gmsh.model.geo.addLine(B, A)
AL = gmsh.model.geo.addLine(A, L)
LK = gmsh.model.geo.addLine(L, K)
KJ = gmsh.model.geo.addLine(K, J)

# Adding the curve loop and surface
gmsh.model.geo.addCurveLoop([JI, IH, HG, GF, FE, ED, DC, CB, BA, AL, LK, KJ], 1)
gmsh.model.geo.addPlaneSurface([1], 1)

gmsh.model.geo.synchronize()

# Adding physical groups for the surface and boundary
surface = gmsh.model.addPhysicalGroup(2, [1], 1)  # Surface as a physical group
boundary = gmsh.model.addPhysicalGroup(1, [JI, IH, HG, GF, FE, ED, DC, CB, BA, AL, LK, KJ],
                                       2)  # Boundary physical group

# Generate the mesh
gmsh.model.mesh.generate(2)

# Run the GUI to visualize

# Collect nodes on the surface and boundary
N, p, t, b = collect_node(order, surface, boundary)

gmsh.fltk.run()
gmsh.finalize()
