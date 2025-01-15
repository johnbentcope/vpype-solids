# Hidden-Line Elimination Algorithm
This is an attempted implementation of Michael Goodrich's Hidden-Line and Hidden-Surface Elimination Algorithms, and Kenneth Clarkson's and Peter Shor's Line-Segment Intersection Algorithm.

## Step 0: _Projecting onto the Image Plane_
### High-Level Description
Objects loaded from file are stored with the following data.

Each record of `OBJ_VERT` corresponds to a vertex `v`, and contains the following fields in the `Vert3D` dataclass:

* the x, y, and z coordinates of `v`
* an adjacency list `ADJACENCIES`, which lists the indices of the edges in `OBJ_EDGE` which are incident to `v`

Each record of `OBJ_FACE` corresponds to a face on the object and contains the following field in the `Face3D` dataclass:

* a list, `BOUNDARY`, of the indices of vertices in `OBJ_VERT` that are on the boundary of the face, in counter clockwise winding

Each record of `OBJ_EDGE` corresponds to an edge `(v, w)`, and contains the following fields in the `Edge3D` dataclass:

* the index of `v` in `OBJ_VERT`
* the index of `w` in `OBJ_VERT`
* the index, `SIDE`, of the face (if any) in `OBJ_FACE` that contains `(v, w)` on its boundary
* the index of the position of `v` in the `BOUNDARY` list of the `SIDE` face
* the index of the position of `w` in the `BOUNDARY` list of the `SIDE` face

In the common case of two adjacent faces sharing an edge, the edge is recorded twice in `OBJ_EDGE`, once for each face to be stored as a `SIDE`.

Transformation and rotation matrices are applied to the vertices of objects in the scene.

Vertices behind the camera are culled, and faces that partially extend behind the camera are clipped. The 3D polygons of the shapes in the scene are projected onto the image plane, using the camera's projection matrix. Before storing these lines, face normals are compared to the vector representing the direction the camera is facing, and this information is used to cull back faces.

## Step 1: _Constructing the Polygon Arrangement_
### High-Level Description
We construct the polygon arrangement of the projected polygons in this step. Since we are dealing with 3D polygons projected to the plane, we augment the polygon arrangement to keep track of some of the 3D information. Namely, for each polygon in `POLY`, we store some additional fields to represent the plane which contains it. A plane containing the polygon can be described by an equation `ax + by + cz + d = 0`, and we will store the coordinates `a`,`b`,`c`, and `d`, as fields in the POLY entry for the polygon to represent the original plane.

The _polygon arrangement_ of the projection plane is defined on the following embedded planar graph `G = (V, E)`:

1. `V` consists of all points `v` that satisfy one of the following:

    (a) `v` is a vertex of a polygon

    (b) `v` is an intersection point of the boundaries of two polygons

    (c) `v` is the vertical shadow of the representative vertex of a polygon

1. `E` consists of all the (undirected) pairs `(v, w)`, (both vertices in `V`):

    (a) `v` and `w` are connected by a polygonal edge `s` and there is no point `z` in `V` between `v` and `w` on `s`

    (b) `w` is the vertical shadow of `v` and `v` is the representative vertex of a polygon

We store the vertices of `V` in an array `VERT`, the edges of `E` in an array `EDGE`, and the polygons in an array `POLY`.

Each record of `VERT` corresponds to a vertex `v`, and contains the following fields in the `Vertex2D` dataclass:

* the x and y coordinates of `v`
* an adjacency list `ADJACENCIES`, which lists the indices of the edges in `EDGE` which are incident to `v`

Each record of `POLY` corresponds to a polygon in the projection plane and contains the following field in the `Poly2D` dataclass:

* a list, `BOUNDARY`, of the indices of vertices in `VERT` that are on the boundary of the polygon, in counter clockwise winding

Each record of `EDGE` corresponds to an edge `(v, w)`, and contains the following fields in the `Edge2D` dataclass:

* the index of `v` in `VERT` (1)
* the index of `w` in `VERT` (1)
* the index, `SIDE`, of the polygon (if any) in `POLY` that contains `(v, w)` on its boundary (2)
* the index of the position of `v` in the `BOUNDARY` list of the `SIDE` polygon (3)
* the index of the position of `w` in the `BOUNDARY` list of the `SIDE` polygon (3)
* a list, `ENTER1`, of the indices of all polygons one enters when traversing `(v, w)` from `v` to `w`
* a list, `ENTER2`, of the indices of all polygons one enters when traversing `(v, w)` from `w` to `v`

Given a set `S` of line segments in the plane, the line segments of `S` are added in random order, one by one, to a set `U`.

An undirected graph, `H(U)` of the following is maintained as `U` grows.
* the intersection points
* the segment endpoints
* the upwards and downwards vertical shadows of segment endpoints and intersection points 

## Step 2: _Computing the Coverage of Representative Vertices_
### High-Level Description
In this step we use the polygon arrangement to compute the _coverage_ of each representative vertex for each polygon.

## Step 3: _Computing Visible Edges_
### High-Level Description
