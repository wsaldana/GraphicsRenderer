from collections import namedtuple

V2 = namedtuple('Vector2', ['x', 'y'])
V3 = namedtuple('Vector3', ['x', 'y', 'z'])

def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
    return V3(
        v0.y * v1.z - v0.z * v1.y,
        v0.z * v1.x - v0.x * v1.z,
        v0.x * v1.y - v0.y * v1.x,
    )