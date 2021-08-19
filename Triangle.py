from collections import namedtuple
from LinearAlgebra import *

V2 = namedtuple('Vector2', ['x', 'y'])
V3 = namedtuple('Vector3', ['x', 'y', 'z'])
Vertices = namedtuple('Vertices', ['A', 'B', 'C'])

class Triangle(object):
    def __init__(self, A, B, C):
        self.vertices = Vertices(V2(A[0],A[1]), V2(B[0],B[1]), V2(C[0],C[1]))
        self.normalized_vertices = self.vertices

    def normalizeTriangle(self):
        values = [c for point in self.vertices for c in point]
        maximo = max(values)
        minimo = min(values)
        normalized_vertices = []
        for point in self.vertices:
            normalized_vertices.append(V2(self.normalize(point[0], maximo, minimo), self.normalize(point[1], maximo, minimo)))
        self.vertices = normalized_vertices

    def getEnclosingBox(self):
        x_values = [c.x for c in self.vertices]
        y_values = [c.y for c in self.vertices]
        return V2(max(x_values), max(y_values)), V2(min(x_values), min(y_values))

    def barycentric(self, P):
        A = self.vertices.A 
        B = self.vertices.B 
        C = self.vertices.C 

        cx, cy, cz = cross(
            V3(B.x - A.x, C.x - A.x, A.x - P.x), 
            V3(B.y - A.y, C.y - A.y, A.y - P.y)
        )

        if abs(cz) < 1:
            return -1, -1, -1
        u = cx/cz
        v = cy/cz
        w = 1 - ((cx+cy)/cz)

        return w, v, u