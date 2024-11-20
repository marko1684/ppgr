import numpy as np
from numpy import linalg  as LA
np.set_printoptions(precision=5, suppress=True)

def correspondence(t, pt):
    Mi = np.matrix([
        [0, 0, 0, -pt[2] * t[0], -pt[2] * t[1], -pt[2] * t[2], pt[1] * t[0], pt[1] * t[1], pt[1] * t[2]],
        [pt[2] * t[0], pt[2] * t[1], pt[2] * t[2], 0, 0, 0, -pt[0] * t[0], -pt[0] * t[1], -pt[0] * t[2]]])
    return Mi

def DLT(points, mapped_points):
    n = len(points)
    M = []

    for i in range(n):
        if i > 0:
            Mi = correspondence(points[i], mapped_points[i])
            M = np.concatenate((M, Mi))
        else:
            M = correspondence(points[i], mapped_points[i])

    U, D, V_tr = LA.svd(M)

    dlt = V_tr[len(V_tr) - 1].reshape(3, 3)
    dlt /= dlt[2, 2] * 1.0
    return dlt
 
import numpy as np
from numpy import linalg
np.set_printoptions(precision=5, suppress=True)
 
def affine_transform(t):
    return [t[0]/t[2], t[1]/t[2]]

def homogeneous_transform(t):
    return [t[0], t[1], 1]

def normMatrix(points):
    n = len(points)

    centroid_x = 0
    centroid_y = 0
    affine_points = []
    for i in range(n):
        affine_points.append(affine_transform(points[i]))
        centroid_x = centroid_x + affine_points[i][0]
        centroid_y = centroid_y + affine_points[i][1]

    centroid_x = centroid_x/n
    centroid_y = centroid_y/n

    O = [[1, 0, -centroid_x],
        [0, 1, -centroid_y],
        [0, 0, 1]
    ]
    for i in range(n):
        affine_points[i] = np.matmul(O, homogeneous_transform(affine_points[i]))

    d = 0 
    for i in range(n):
        tmp = np.square(affine_points[i][0]) + np.square(affine_points[i][1])
        d = d + np.sqrt(tmp)
    d = d/n

    H = [
        [np.sqrt(2)/d, 0, 0],
        [0, np.sqrt(2)/d, 0],
        [0, 0, 1]
    ]
    for i in range(n):
        affine_points[i] = np.matmul(H, homogeneous_transform(affine_points[i]))

    return np.matmul(H, O)

trapez = [[- 3, - 1, 1], [3, - 1, 1], [1, 1, 1], [- 1, 1, 1], [1,2,3], [-8,-2,1]] 
print(normMatrix(trapez))