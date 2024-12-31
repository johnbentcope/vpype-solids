import click
import numpy as np
import vpype as vp
import vpype_cli
import tinyobjloader
from typing import Iterator, Tuple

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

def process_shape(shape, attrib):
  unique_lines = set()
  indices = shape.mesh.vertex_indices()
  face_sizes = shape.mesh.num_face_vertices
  current_idx = 0
  for face_size in face_sizes:
    face_lines = get_face_lines(indices, current_idx, face_size)
    unique_lines.update(face_lines)
    current_idx += face_size

  return list(unique_lines)

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
@click.option("-w", "--width", type=float, default=-1.0)
@click.option("-h", "--height", type=float, default=-1.0)
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

  # Debug prints, remove someday
  print(f"document: {document}")
  print(f"filename: {filename}")
  # print(f"translation: {translation}")
  # print(f"rotation: {rotation}")
  print(f"layer: {layer}")
  # print(f"eye_x: {eye_x}")
  # print(f"eye_y: {eye_y}")
  # print(f"eye_z: {eye_z}")
  # print(f"look_x: {look_x}")
  # print(f"look_y: {look_y}")
  # print(f"look_z: {look_z}")
  # print(f"up_x: {up_x}")
  # print(f"up_y: {up_y}")
  # print(f"up_z: {up_z}")
  print(f"fov: {fov}")
  print(f"z_near: {z_near}")
  print(f"z_far: {z_far}")
  print(f"aspect: {aspect}")
  print(f"width: {width}")
  print(f"height: {height}")

  # # Calculate aspect ratio if needed
  # if aspect <= 0:
  #   bounds = document.bounds()
  #   if bounds is not None:
  #     aspect = bounds[2] / bounds[3]
  #   else:
  #     aspect = 1.0

  attrib = reader.GetAttrib()

  numpy_verts = attrib.numpy_vertices()
  numpy_verts = numpy_verts.reshape(-1, 3)

  shapes = reader.GetShapes()

  for shape in shapes:
    print(shape.name)

    unique_lines = process_shape(shape, attrib)

    # Debug: Use direct x,y coords instead of projection
    for line in unique_lines:
      v1 = numpy_verts[line.v1_idx]
      v2 = numpy_verts[line.v2_idx]
      # Convert to complex numbers (x + yi)
      c1 = complex(v1[0], -v1[2])
      c2 = complex(v2[0], -v2[2])

      lc.append([(c1, c2)])

    print(f"lc = {lc.segment_count()}")

  document.add(lc, target_layer)
  return document

vpype_solids.help_group = "Input"
