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
gl.glClearColor(0,0,0)
gl.glClear()
gl.glViewPort(0, 0, 1000, 1000)
gl.glColor(0,1,0)
#gl.glVertex(-0.5, -0.5)
#gl.glLine(-0.9, 0.4, -0.1, 0.6)
#gl.load("Pokemon.obj", (800, 200, 0), (700, 700, -700))
#gl.triangle((10, 70), (50, 160), (70, 80))
#gl.triangle((-0.5, 0), (0, -0.5), (0.5, 0.5))
#gl.earth()
#gl.load("earth.obj", (300, 1200, 0), (0.25, 0.25, 0.25))


#gl.texture(Texture('./Face/model.bmp'))
gl.texture(Texture('ivy.bmp'))
gl.lookAt((1, 0, 5), (0, 0, 0), (0, 1, 0))
gl.load("Pokemon.obj", (0, -0.7, 0), (0.4, 0.4, -0.4), (0,0,0))

gl.draw_arrays()

gl.glFinish('render1')