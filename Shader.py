import random
from utils import color
from LinearAlgebra import dot

def gourad(render, **kwargs):
    w, v, u = kwargs['bar']
    nA, nB, nC = kwargs['varying_normals']
    
    if render.current_texture:
      tx, ty = kwargs['texture_coords']
      tcolor = render.current_texture.getColor(tx, ty)
    else:
      tcolor = render.current_color

    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    
    intensity = w*iA + v*iB + u*iC
    
    return color(
      int(tcolor[2] * intensity) if tcolor[0] * intensity >= 0 else 0,
      int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
      int(tcolor[0] * intensity) if tcolor[2] * intensity >= 0 else 0
    )