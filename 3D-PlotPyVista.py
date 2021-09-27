import pyvista as pv
import numpy as np

# Define the nodes
pts = np.array([(-5.795555, -4, 1.55291), (-4.829629, -2, 1.294095),
       (-5.795555, 1, 1.552914), (-5.536736, -4, 2.51884),
       (-4.57081, -2, 2.260021), (-5.536736,  1, 2.51884)])
# Define the quads
faces = np.array([(4,0,3,4,1), (4,1,4,5,2)])

# Instantiate a mesh
mesh = pv.PolyData(pts, faces)

# Create a plotting window and display!
p = pv.Plotter()

# Add the mesh and some labels
p.add_mesh(mesh, show_edges=True)
p.add_point_labels(mesh.points, ["%d"%i for i in range(mesh.n_points)])

# A pretty view position
p.camera_position = [(-11.352247399703748, -3.421477319390501, 9.827830270231935),
 (-5.1831825, -1.5, 1.9064675),
 (-0.48313206526616853, 0.8593146723923926, -0.16781448484204659)]

# Render it!
p.show()