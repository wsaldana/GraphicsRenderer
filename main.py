'''
UNIVERSIDAD DEL VALLE DE GUATEMALA
Gráficas por computadoras #10
Walter Saldaña #19897
'''

from MyGL import MyGL
from Polygon import Polygon
from Texture import Texture

gl = MyGL()
gl.glInit()
gl.glCreateWindow(1000, 1000)
gl.glClearColor(0.3,0.3,0.8)
gl.glClear()
gl.glViewPort(0, 0, 1000, 1000)
gl.glColor(0,1,0)

gl.background()

gl.lookAt((1, 0, 5), (0, 0, 0), (0, 1, 0))

gl.texture(Texture('./Models/ivy.bmp'))
gl.load("./Models/Pokemon.obj", (0, -0.7, 0), (0.4, 0.4, -0.4), (0,0,0))
gl.draw_arrays()

gl.texture(Texture('./Models/mew.bmp'))
gl.load("./Models/mew2.obj", (-0.3, 0.1, 0), (0.15, 0.15, 0.15), (0.7,0,0))
gl.draw_arrays()

gl.texture(Texture('./Models/charizard2.bmp'))
gl.load("./Models/charizard3.obj", (0.4, -0.7, -2), (0.08, 0.08, 0.08), (0,0,0))
gl.draw_arrays()

gl.texture(Texture('./Models/lego.bmp'))
gl.load("./Models/lego2.obj", (-0.5, -0.2, 0.5), (0.4, 0.4, 0.4), (0,0,0))
gl.draw_arrays()

gl.texture(Texture('./Models/pokeball.bmp'))
gl.load("./Models/pokeball.obj", (-0.3, -0.4, 0.53), (0.05, 0.05, 0.05), (0,0,0))
gl.draw_arrays()

gl.draw_arrays()

gl.glFinish('render1')