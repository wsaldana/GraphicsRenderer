class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.tvertices = []
        self.normales = []
        self.faces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line and (line[0] != '#'):
                try:
                    prefix, value = line.split(' ', 1)
                except:
                    prefix = ''

                if prefix == 'v':
                    self.vertices.append(
                        list(map(float, value.split(' ')))
                    )
                elif prefix == 'vt':
                    vts = value.split(' ')
                    if len(vts)==3:
                        self.tvertices.append(
                            list(map(float, value.split(' ')))
                        )
                    else:
                        self.tvertices.append(
                            list(map(float, value.split(' '))) + [0.0000]
                        )
                elif prefix == 'vn':
                    self.normales.append(
                        list(map(float, value.split(' ')))
                    )
                elif prefix == 'f':
                    faces = value.split(' ')
                    
                    for i in range(len(faces)-2):
                        triangle = [faces[0], faces[i+1], faces[i+2]]
                        self.faces.append(
                            [list(map(int, face.split('/'))) for face in triangle if len(face)>2]
                        )