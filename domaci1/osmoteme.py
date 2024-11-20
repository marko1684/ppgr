import math

def cross(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    
    cross_x = y1 * z2 - z1 * y2  
    cross_y = z1 * x2 - x1 * z2  
    cross_z = x1 * y2 - y1 * x2  
    
    return (cross_x, cross_y, cross_z)  

def normalize_point(point):
    epsilon = 1e-9
    x, y, z = point
    if abs(z) < epsilon:
        return (x, y, 1)  
    return (x / z, y / z, 1)

def osmoteme(points):
    for x in points:
        x.append(1)  
    
    points = [normalize_point(p) for p in points if p is not None]

    if len(points) < 7:
        return None

    Xb = cross(cross(points[5], points[1]), cross(points[4], points[0]))
    Xb = normalize_point(Xb)

    Yb = cross(cross(points[0], points[1]), cross(points[2], points[3]))
    Yb = normalize_point(Yb)

    Yb1 = cross(cross(points[5], points[4]), cross(points[2], points[3]))
    Yb1 = normalize_point(Yb1)

    Yb2 = cross(cross(points[5], points[4]), cross(points[1], points[0]))
    Yb2 = normalize_point(Yb2)

    Xb1 = cross(cross(points[5], points[1]), cross(points[6], points[2]))
    Xb1 = normalize_point(Xb1)

    Xb2 = cross(cross(points[4], points[0]), cross(points[6], points[2]))
    Xb2 = normalize_point(Xb2)

    Xb = ((Xb1[0] + Xb2[0] + Xb[0]) / 3, (Xb1[1] + Xb2[1] + Xb[1]) / 3, 1)
    Yb = ((Yb1[0] + Yb2[0] + Yb[0]) / 3, (Yb1[1] + Yb2[1] + Yb[1]) / 3, 1)

    missing_point = cross(cross(points[3], Xb), cross(points[6], Yb))
    missing_point = normalize_point(missing_point)
    
    return [math.floor(missing_point[0]), math.floor(missing_point[1])]


# t5, t6, t7, t8, t1, t2, t3
# tacke = [[32, 70], [195, 144], [195, 538], [30, 307], [251, 40], [454, 78], [455, 337]]
tacke = [[639, 125], [472, 306], [131, 175], [407, 79], [605, 292], [445, 555], [166, 384]]
print(osmoteme(tacke))
