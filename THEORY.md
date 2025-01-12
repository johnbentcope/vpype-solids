# Hidden-Line Elimination Algorithm
## Step 1: _Constructing the Polygon Arrangement_
### High-Level Description
We construct the polygon arrangement of the projected polygons in this step. Since we are dealing with 3D polygons projected to the plane, we augment the polygon Arrangement to keep track of some of the 3D information. Namely, for each polygon in POLY, we store some additional fields to represent the plane which contains it. A plane containing the polygon can be described by an equation `ax + by + cz + d = 0`, and we will store the coordinates `a`,`b`,`c`, and `d`, as fields in the POLY entry for the polygon to represent the original plane.

The _polygon arrangement_ of the projection plane is defined on the following embedded planar graph `G = (V, E)`:

1. `V` consists of all points `v` that satisfy one of the following:

    (a) `v` is a vertex of a polygon

    (b) `v` is an intersection point of the boundaries of two polygons

    (c) `v` is the vertical shadow of the representative vertex of a polygon

1. E consists of all the (undirected) pairs `(v, w)`, (both vertices in `V`):

    (a) `v` and `w` are connected by a polygonal edge `s` and there is no point `z` in `V` between `v` and `w` on `s`

    (b) `w` is the vertical shadow of `v` and `v` is the representative vertex of a polygon

We store the vertices of `V` in an array `VERT`, the edges of `E` in an array `EDGE`, and the polygons in an array `POLY`.

Each record of `VERT` corresponds to a vertex `v`, and contains the following fields:

* the x and y coordinates of `v`
* an adjacency list `ADJACENCIES`

Each record of `POLY` corresponds to a polygon in the projection plane and contains the following field:

* a list, `BOUNDARY`, of the indices of vertices in `VERT` that are on the boundary of the polygon

Each record of `EDGE` corresponds to an edge `(v, w)`, and contains the following fields:

* the index of `v` in `VERT`
* the index of `w` in `VERT`
* the index, `SIDE`, of the polygon (if any) in `POLY` that contains `(v, w)` on its boundary
* the index of the position of `v` in the `BOUNDARY` list of the `SIDE` polygon
* the index of the position of `w` in the `BOUNDARY` list of the `SIDE` polygon


Given a set `S` of line segments in the plane, the line segments of `S` are added in random order, one by one, to a set `U`. An undirected graph, `H(U)` of the intersection points, the segment endpoints, and the upwards and downwards vertical shadows of segment endpoints and intersection points is maintained as `U` grows.

## Step 2: _Computing the Coverage of Representative Vertices_
### High-Level Description
In this step we use the polygon arrangement to compute the _coverage_ of each representative vertex for each polygon.

## Step 3: _Computing Visible Edges_
### High-Level Description
