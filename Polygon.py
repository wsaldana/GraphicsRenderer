class Polygon(object):
    
    def __init__(self, vertices):
        self.vertices = vertices
        self.normalized_vertices = []
        self.perimeter = []
        
    def normalize(self, n, maximo, minimo):
        return (n-minimo)/(maximo-minimo)
    
    def normalizePolygon(self, vertices=None):
        values = [c for point in vertices for c in point]
        maximo = max(values)
        minimo = min(values)
        normalized = []
        for point in vertices:
            normalized.append((self.normalize(point[0], maximo, minimo), self.normalize(point[1], maximo, minimo)))
        self.normalized_vertices = normalized
        
    def normalizePolygons(self, polygons):
        #joined = [point for polygon in polygons for point in polygon]
        values = [c for point in [point for polygon in polygons for point in polygon] for c in point]
        maximo = max(values)
        minimo = min(values)
        normalized = []
        for polygon in polygons:
            new_polygon = []
            for point in polygon:
                new_polygon.append((self.normalize(point[0], maximo, minimo), self.normalize(point[1], maximo, minimo)))
            normalized.append(new_polygon)
        return normalized