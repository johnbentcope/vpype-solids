import click
import numpy as np
import vpype as vp
import vpype_cli
import tinyobjloader
from dataclasses import dataclass
from typing import Iterator, List, Tuple

from vpype_cli.types import LayerType,LengthType

class Line:
  def __init__(self, v1_idx: int, v2_idx: int):
    self.v1_idx = v1_idx
    self.v2_idx = v2_idx
    self.normal = None # Eventually need to calculate "normals" of lines from adjacent faces

  def __str__(self) -> str:
    normal_str = f", n={self.normal}" if self.normal is not None else ""
    return f"Line({self.v1_idx}->{self.v2_idx}{normal_str})"

  def __repr__(self) -> str:
    return f"Line(v1_idx={self.v1_idx}, v2_idx={self.v2_idx}, normal={self.normal})"

  def __eq__(self, other):
    # Lines are equal if they have same vertices in any order
    return (self.v1_idx == other.v1_idx and self.v2_idx == other.v2_idx) or \
            (self.v1_idx == other.v2_idx and self.v2_idx == other.v1_idx)

  def __hash__(self):
    # Hash should be same for both vertex orderings
    return hash(frozenset([self.v1_idx, self.v2_idx]))

def get_face_lines(indices, face_start: int, num_vertices: int) -> list[Line]:
  lines = []
  for i in range(num_vertices):
    v1 = indices[face_start + i]
    v2 = indices[face_start + ((i + 1) % num_vertices)]
    lines.append(Line(v1, v2))
  for line in lines:
    # print(f"Adding line to lines from ({line.v1_idx}) to ({line.v2_idx})")
    pass
  return lines

def process_shape(shape):
  unique_lines = set()
  indices = shape.mesh.vertex_indices()
  face_sizes = shape.mesh.num_face_vertices
  current_idx = 0
  for face_size in face_sizes:
    face_lines = get_face_lines(indices, current_idx, face_size)
    unique_lines.update(face_lines)
    current_idx += face_size

  return list(unique_lines)

def generate_projection_matrix(aspect, fov, z_near, z_far):
  f = 1 / np.tan(np.radians(fov)/2.0)
  q = (z_far)/(z_far-z_near)
  if (z_near == z_far):
    print("Cannot compute a null frustum.")
    return None
  proj_matrix = np.matrix([
    [  aspect*f,         0,         0,         0],
    [         0,         f,         0,         0],
    [         0,         0,         q,         1],
    [         0,         0, -z_near*q,         0]
  ])
  return proj_matrix

@click.command()
@click.option("--filename",type=vpype_cli.PathType(exists=True), required=True)
# @click.option("-t", "--translation", type=float, default=-1.0)
# @click.option("-r", "--rotation", type=float, default=-1.0)
@click.option(
  "-l",
  "--layer",
  type=LayerType(accept_new=True),
  default=1,
  help="Layer for object's line art (default: 1)."
)
# @click.option("-x", "--eye-x", type=float, default=0.0)
# @click.option("-y", "--eye-y", type=float, default=0.0)
# @click.option("-z", "--eye-z", type=float, default=0.0)
# @click.option("-a", "--look-x", type=float, default=0.0)
# @click.option("-b", "--look-y", type=float, default=0.0)
# @click.option("-c", "--look-z", type=float, default=1.0)
# @click.option("-m", "--up-x", type=float, default=0.0)
# @click.option("-n", "--up-y", type=float, default=-1.0)
# @click.option("-o", "--up-z", type=float, default=0.0)
@click.option("-f", "--fov", type=float, default=90.0)
@click.option("--z_near", type=float, default=0.01)
@click.option("--z_far", type=float, default=1000.0)
@click.option("--aspect", type=float, default=-1.0)   
@click.option("-w", "--width", type=LengthType(), default=-1.0)
@click.option("-h", "--height", type=LengthType(), default=-1.0)
@vpype_cli.global_processor

def vpype_solids(document: vp.Document, filename: str,
                #  translation: str, rotation: str,
                 layer: int,
                #  eye_x: float, eye_y: float, eye_z: float, look_x: float, look_y: float, look_z: float, up_x: float, up_y: float, up_z: float,
                 fov: float, z_near: float, z_far: float,
                 aspect: float, width: float, height: float
                 ):
  """
  Load OBJ files into vpype.
  """

  # Setting up vpype-intrinsics
  target_layer = vpype_cli.single_to_layer_id(layer, document)
  lc = vp.LineCollection()

  # Attempt loading OBJ file, make work for multiple files someday
  reader = tinyobjloader.ObjReader()
  ret = reader.ParseFromFile(filename)
  if not ret:
    raise click.ClickException("Failed to load file")

  if ((width > 0 and height > 0 and aspect > 0) or  # W H A
      width == 0 or height == 0 or aspect == 0):
    print("Failure calculating aspect ratio.")
    raise SystemExit()
  if width > 0:
    if height > 0:                                  # W H a
      aspect = width/height
    elif aspect > 0:                                # W h A
      height = width / aspect
    else:                                           # W h a
      height = width
      aspect = 1.0
  if height > 0:
    if aspect > 0:                                  # w H A
      width =  height * aspect
    else:                                           # w H a
      width = height
      aspect = 1.0

  # # Debug prints, remove someday
  # print(f"document: {document}")
  # print(f"filename: {filename}")
  # # print(f"translation: {translation}")
  # # print(f"rotation: {rotation}")
  # print(f"layer: {layer}")
  # # print(f"eye_x: {eye_x}")
  # # print(f"eye_y: {eye_y}")
  # # print(f"eye_z: {eye_z}")
  # # print(f"look_x: {look_x}")
  # # print(f"look_y: {look_y}")
  # # print(f"look_z: {look_z}")
  # # print(f"up_x: {up_x}")
  # # print(f"up_y: {up_y}")
  # # print(f"up_z: {up_z}")
  print(f"fov: {fov}")
  print(f"z_near: {z_near}")
  print(f"z_far: {z_far}")
  print(f"aspect: {aspect}")
  print(f"width: {width}")
  print(f"height: {height}")

  proj_matrix = generate_projection_matrix(aspect, fov, z_near, z_far)
  print(f"proj_matrix = \n{proj_matrix}")

  attrib = reader.GetAttrib()

  numpy_verts = attrib.numpy_vertices()
  numpy_verts = numpy_verts.reshape(-1, 3)
  print(f"numpy_verts:\n{numpy_verts}")

  shapes = reader.GetShapes()

  for shape in shapes:
    print(shape.name)

    VERT    = []
    EDGE    = []
    POLY    = []
    COMP    = []

    # print("len(num_indices) = {}".format(len(shape.mesh.indices)))
    for i, idx in enumerate(shape.mesh.indices):
      print(f"[{i}] v_idx {idx.vertex_index:2}")
    
    temp = np.array([numpy_verts[0][0],numpy_verts[0][1],numpy_verts[0][2],1]) @ proj_matrix
    temp = np.array([temp[0,0], temp[0,1], temp[0,2]])/temp[0,3]
    print(f"projected {numpy_verts[0]} is {temp}")

    # face_boundary_lengths = shape.mesh.num_face_vertices
    # print(f"face sizes: {face_boundary_lengths}")

    # indices = shape.mesh.vertex_indices()
    # print(f"indices: {indices}")

    # current_idx = 0
    # for face_size in face_boundary_lengths:
    #   face_lines = get_face_lines(indices, current_idx, face_size)
    #   unique_lines.update(face_lines)
    #   current_idx += face_size

  #   unique_lines = process_shape(shape)

  #   # Debug: Use direct x,y coords instead of projection
  #   for line in unique_lines:
  #     v1 = numpy_verts[line.v1_idx]
  #     v2 = numpy_verts[line.v2_idx]
  #     # Convert to complex numbers (x + yi)
  #     c1 = complex(v1[0], -v1[2])
  #     c2 = complex(v2[0], -v2[2])

  #     lc.append([(c1, c2)])

  #   print(f"lc = {lc.segment_count()}")

  # document.add(lc, target_layer)
  return document

vpype_solids.help_group = "Input"

# Each record of VERT corresponds to a vertex v, and contains the following fields:
@dataclass
class Vertex2D:
  coordinates:  tuple[float, float]  # the x and y coordinates of v
  adjacencies:  List[int]            # an adjacency list ADJACENCIES, which lists the indices of the edges in EDGE which are incident to v

# Each record of VERT corresponds to a vertex v, and contains the following fields:
@dataclass
class Vertex3D:
  coordinates:  tuple[float, float, float]  # the x, y, and z coordinates of v
  adjacencies:  List[int]                   # an adjacency list ADJACENCIES, which lists the indices of the edges in EDGE which are incident to v

# Each record of EDGE corresponds to an edge (v, w), and contains the following fields:
@dataclass
class Edge2D:
  v_index_v:  int       # the index of v in VERT
  w_index_v:  int       # the index of w in VERT
  side:       int       # the index, SIDE, of the polygon (if any) in POLY that contains (v, w) on its boundary
  v_index_s:  int       # the index of the position of v in the BOUNDARY list of the SIDE polygon
  w_index_s:  int       # the index of the position of w in the BOUNDARY list of the SIDE polygon
  enter1:     List[int] # an adjacency list ADJACENCIES, which lists the indices of the edges in EDGE which are incident to v
  enter2:     List[int] # an adjacency list ADJACENCIES, which lists the indices of the edges in EDGE which are incident to v

# Each record of EDGE corresponds to an edge (v, w), and contains the following fields:
@dataclass
class Edge3D:
  v_index_v:  int       # the index of v in VERT
  w_index_v:  int       # the index of w in VERT
  side:       int       # the index, SIDE, of the face (if any) in POLY that contains (v, w) on its boundary
  v_index_s:  int       # the index of the position of v in the BOUNDARY list of the SIDE face
  w_index_s:  int       # the index of the position of w in the BOUNDARY list of the SIDE face

# Each record of POLY corresponds to a polygon in the projection plane and contains the following field:
@dataclass
class Poly2D:
  boundary:     List[int] # a list, BOUNDARY, of the indices of vertices in VERT that are on the boundary of the polygon, in counter clockwise winding
  coordinates:  List[int] # For storing [a, b, c, d] for the planar equation ax + by + cz + d = 0

# Each record of POLY corresponds to a polygon in the projection plane and contains the following field:
@dataclass
class Face3D:
  boundary:     List[int] # a list, BOUNDARY, of the indices of vertices in VERT that are on the boundary of the polygon, in counter clockwise winding
  coordinates:  List[int] # For storing [a, b, c, d] for the planar equation ax + by + cz + d = 0
